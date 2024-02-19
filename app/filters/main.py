import os
import re
from flask import current_app
from googleapiclient import discovery
from services.words import list_bad_words, increment_occurrence
from services.phrases import get_single_phrase, insert_bad_phrase, get_phrase_languages, insert_bad_phrase_languages, increment_occurrence as phrase_increment_occurrence


# Function to get detected languages and their codes for a given phrase
def get_phrase_languages_and_codes(phrase_id):
    """Returns detected languages and their codes for a given phrase ID."""
    detected_languages_ids = set()
    detected_languages_codes = set()

    languages = get_phrase_languages(phrase_id)
    if languages is not None:
        for lang in languages:
            detected_languages_ids.add(lang['id'])
            detected_languages_codes.add(lang['code'])

    return detected_languages_ids, detected_languages_codes


def filter_bad_words(text):  # Function to filter bad words from text
    """Filters bad words from the given text.

    Args:
        text (str): The text to be filtered for bad words.

    Returns:
        tuple: A tuple containing the filtered text, the count of matched bad words,
               and a list of detected language codes.
    """
    global detected_languages_ids
    detected_languages_ids = set()
    detected_languages_codes = set()

    # Check if the text matches any existing phrase
    matched_phrase = get_single_phrase(("phrase", text))
    if matched_phrase is not None:
        # Increment occurrence count of the matched phrase
        phrase_increment_occurrence(matched_phrase)
        # Get detected languages and their codes for the matched phrase
        detected_languages_ids, detected_languages_codes = get_phrase_languages_and_codes(
            matched_phrase["id"]
        )
        return matched_phrase["filtered_phrase"], matched_phrase["total_bad_words"], list(detected_languages_codes)

    global matched_words_count
    matched_words_count = 0
    # Get the list of bad words
    bad_words = list_bad_words()

    # Define pattern for matching bad words
    pattern = r'\b(?:' + '|'.join(re.escape(word["word"].strip())
                                  for word in bad_words) + r')\b'

    # Function to replace bad words in the text
    def replace_word(match):
        global matched_words_count, detected_languages_ids

        word = match.group()

        matched_words_count += 1

        # Increment occurrence count of the matched bad word and add its language ID
        for word_row in bad_words:
            if word_row['word'] == word:
                increment_occurrence(word_row)
                detected_languages_ids.add(word_row['lang_id'])

        return word[0] + '*' * (len(word) - 1)

    # Replace bad words in the text using the defined pattern and replacement function
    filtered_text = re.sub(pattern, replace_word, text, flags=re.IGNORECASE)

    # Insert the filtered text into the database and get its phrase ID
    phrase_id = insert_bad_phrase(text, filtered_text, current_app.config['project_id'],
                                  matched_words_count)

    # Print detected language IDs for debugging purposes
    print(detected_languages_ids)

    # Insert detected language IDs into the database for the filtered text
    insert_bad_phrase_languages(phrase_id, detected_languages_ids)

    # Get detected languages and their codes for the filtered text
    detected_languages_ids, detected_languages_codes = get_phrase_languages_and_codes(
        phrase_id)

    return filtered_text, matched_words_count, list(detected_languages_codes)


# Function to get Google Perspective API score for text
def google_perspective_score(text):
    """Gets Google Perspective API score for the given text."""
    API_KEY = os.environ.get('GOOGLE_API_KEY')

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response["attributeScores"]["TOXICITY"]["summaryScore"]
