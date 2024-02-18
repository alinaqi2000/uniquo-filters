import sqlite3
from .utils import get_db_connection


def insert_row(table: str, data: dict):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in range(len(data))])
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    return execute_query(query, tuple(data.values()))


def update_data(table: str, set_values: dict, condition: tuple):
    """Update data in a table."""
    set_clause = ', '.join([f"{column} = ?" for column in set_values.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition[0]} = ?"
    execute_query(query, tuple(set_values.values()) + (condition[1],))


def select_rows(table: str,  params: tuple = ()):
    return execute_read_query(f"SELECT * FROM {table}", params)


def select_row(table: str,  condition: tuple):
    return execute_read_query(f"SELECT * FROM {table} WHERE {condition[0]} = ?", (condition[1],), True)


def count_rows(table: str,  condition: tuple = ()):
    if condition == ():
        return execute_read_query(f"SELECT count(*) as total FROM {table}", (), True)

    return execute_read_query(f"SELECT count(*) as total FROM {table} WHERE {condition[0]} = ?", (condition[1],), True)


def delete_row(table: str,  condition: tuple = ()):
    return execute_query(f"DELETE FROM {table} WHERE {condition[0]} = ?", (condition[1],), True)


def execute_query(query, params=()):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def execute_read_query(query, params=(), single=False):
    conn = get_db_connection()
    result = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone() if single else cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
