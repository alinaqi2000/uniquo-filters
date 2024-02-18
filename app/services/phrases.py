import sqlite3
from .crud import *

TABLE_NAME = "bad_phrases"


def get_single_phrase(condition=()):
    return select_row(TABLE_NAME, condition)


def list_bad_phrases():
    return select_rows(TABLE_NAME)


def count_bad_phrases(condition=()):
    return count_rows(TABLE_NAME, condition)


def insert_bad_phrase(phrase: str, filtered_phrase: str, project_id=0, total_bad_words=1, total_occurrences=1):
    return insert_row(TABLE_NAME, {
        "phrase": phrase, "filtered_phrase": filtered_phrase, "project_id": project_id, "total_bad_words": total_bad_words, "total_occurrences": total_occurrences})


def increment_occurrence(phrase: sqlite3.Row):
    return update_data(TABLE_NAME, {"total_occurrences": phrase["total_occurrences"] + 1}, ("id", phrase['id']))
