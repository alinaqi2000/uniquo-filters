from db.models import BadWord
from db.config import db


def list_bad_words(condition=()):
    return BadWord.query.filter(*condition).all()


def count_bad_words(condition=()):
    return BadWord.query.filter(*condition).count()


def increment_occurrence(word: BadWord):
    word.total_occurrences += 1
    db.session.commit()
    return word


def insert_bad_word(word: str, project_id, language_id, occurrence=1):
    bad_word = BadWord(word=word, project_id=project_id,
                       lang_id=language_id, total_occurrences=occurrence)
    try:
        db.session.add(bad_word)
        db.session.commit()

    except Exception as e:
        print(f"Error committing changes to the database: {e}")
        db.session.rollback()
    finally:
        return bad_word
