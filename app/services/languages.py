import sqlite3
from .crud import *

TABLE_NAME = "languages"


def get_single_language(condition=()):
    return select_row(TABLE_NAME, condition)


def list_languages():
    return select_rows(TABLE_NAME)


def count_languages(condition=()):
    return count_rows(TABLE_NAME, condition)


def language_exists(code: str) -> bool:
    language = count_rows(TABLE_NAME, ("code", code))
    return language != None and language['total'] > 0


def insert_language(code: str, name: str):
    return insert_row(TABLE_NAME, {"code": code, "name": name})
