import sqlite3
from .crud import *

TABLE_NAME = "bad_words"


def list_bad_words(condition=()):
    return select_rows(TABLE_NAME, condition)


def count_bad_words(condition=()):
    return count_rows(TABLE_NAME, condition)


def increment_occurrence(word: sqlite3.Row):
    return update_data(TABLE_NAME, {"total_occurrences": word["total_occurrences"] + 1}, ("id", word['id']))


def insert_bad_word(word: str, project_id, language_id, occurrence=1):
    return insert_row(TABLE_NAME, {
        "word": word, "project_id": project_id, "lang_id": language_id, "total_occurrences": occurrence})
