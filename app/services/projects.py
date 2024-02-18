import sqlite3
from .crud import *

TABLE_NAME = "projects"


def get_single_project(condition=()):
    return select_row(TABLE_NAME, condition)


def list_projects():
    return select_rows(TABLE_NAME)


def count_projects(condition=()):
    return count_rows(TABLE_NAME, condition)


def project_exists(code: str) -> bool:
    project = count_rows(TABLE_NAME, ("code", code))
    return project != None and project['total'] > 0


def insert_project(code: str, name: str):
    return insert_row(TABLE_NAME, {"code": code, "name": name})
