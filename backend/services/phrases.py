from db.models import PhraseLanguage, BadPhrase, Language
from db.config import db


def get_single_phrase(condition=()):
    return BadPhrase.query.filter(*condition).first()


def list_bad_phrases(condition=()):
    return BadPhrase.query.filter(*condition).all()


def get_phrase_languages(phrase_id):
    return db.session.query(Language).join(PhraseLanguage, Language.id == PhraseLanguage.lang_id).filter(PhraseLanguage.phrase_id == phrase_id).all()


def count_bad_phrases(condition=()):
    return BadPhrase.query.filter(*condition).count()


def insert_bad_phrase(phrase: str, filtered_phrase: str, project_id=0, total_bad_words=1, total_occurrences=1):
    bad_phrase = BadPhrase(phrase=phrase, filtered_phrase=filtered_phrase, project_id=project_id,
                           total_bad_words=total_bad_words, total_occurrences=total_occurrences)
    db.session.add(bad_phrase)
    db.session.commit()
    return bad_phrase


def insert_bad_phrase_languages(phrase_id, language_ids):
    for lang_id in language_ids:
        phrase_language = PhraseLanguage(phrase_id=phrase_id, lang_id=lang_id)
        db.session.add(phrase_language)
    db.session.commit()


def increment_occurrence(phrase: BadPhrase):
    phrase.total_occurrences += 1
    db.session.commit()
    return phrase
