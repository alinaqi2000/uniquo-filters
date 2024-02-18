import os
import re
from flask import current_app
from googleapiclient import discovery
from services.words import list_bad_words, increment_occurrence
from services.phrases import get_single_phrase, insert_bad_phrase, increment_occurrence as prase_increment_occurrence


def filter_bad_words(text):

    matched_phrase = get_single_phrase(("phrase", text))
    if matched_phrase is not None:
        prase_increment_occurrence(matched_phrase)
        return matched_phrase["filtered_phrase"], matched_phrase["total_bad_words"]

    global matched_words_count
    matched_words_count = 0
    bad_words = list_bad_words()

    pattern = r'\b(?:' + '|'.join(re.escape(word["word"].strip())
                                  for word in bad_words) + r')\b'

    def replace_word(match):
        word = match.group()

        global matched_words_count
        matched_words_count += 1

        for word_row in bad_words:
            increment_occurrence(
                word_row) if word_row['word'] == word else None

        return word[0] + '*' * (len(word) - 1)

    filtered_text = re.sub(pattern, replace_word, text, flags=re.IGNORECASE)

    insert_bad_phrase(text, filtered_text, current_app.config['project_id'],
                      matched_words_count)

    return filtered_text, matched_words_count


def google_perspective_score(text):

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
