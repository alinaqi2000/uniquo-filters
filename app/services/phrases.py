import sqlite3
from .crud import *
from .languages import TABLE_NAME as LANGUAGE_TABLE_NAME
TABLE_NAME = "bad_phrases"
PHRASE_LANGUAGE_TABLE_NAME = "phrase_languages"


def get_single_phrase(condition=()):
    return select_row(TABLE_NAME, condition)


def list_bad_phrases(condition=()):
    return select_rows(TABLE_NAME, condition)


def get_phrase_languages(phrase_id):
    return execute_read_query(f"""SELECT l.* from {PHRASE_LANGUAGE_TABLE_NAME} pl
                              JOIN {LANGUAGE_TABLE_NAME} l ON pl.lang_id = l.id
                              WHERE pl.phrase_id = {phrase_id}""")


def count_bad_phrases(condition=()):
    return count_rows(TABLE_NAME, condition)


def insert_bad_phrase(phrase: str, filtered_phrase: str, project_id=0, total_bad_words=1, total_occurrences=1):
    return insert_row(TABLE_NAME, {
        "phrase": phrase, "filtered_phrase": filtered_phrase, "project_id": project_id, "total_bad_words": total_bad_words, "total_occurrences": total_occurrences})


def insert_bad_phrase_languages(phrase_id, language_ids):
    for lang_id in language_ids:
        insert_row(PHRASE_LANGUAGE_TABLE_NAME, {
                   "phrase_id": phrase_id, "lang_id": lang_id})


def increment_occurrence(phrase: sqlite3.Row):
    return update_data(TABLE_NAME, {"total_occurrences": phrase["total_occurrences"] + 1}, ("id", phrase['id']))
