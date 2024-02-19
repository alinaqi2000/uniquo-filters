from services.utils import get_db_connection, read_bad_words
from services.words import insert_bad_word, list_bad_words, count_bad_words
from services.projects import insert_project, count_projects
from services.languages import insert_language, language_exists, get_single_language


def seed_database():
    count = count_projects()
    project_id = 0
    if count["total"] == 0:
        project_id = insert_project("uniquo1", "Uniquo")
        print("Sample project inserted into the database!")
    else:
        print("Sample project is already loaded!")

    count = count_bad_words()
    if count["total"] == 0:
        languages, bad_words_data = read_bad_words()

        for language_code in bad_words_data:
            if not language_exists(language_code):
                language_id = insert_language(
                    language_code, languages[language_code].rstrip())
            else:
                language = get_single_language(("code", language_code))
                language_id = language['id']

            for word in bad_words_data[language_code]:
                insert_bad_word(word, project_id, language_id, 0)

        print("Bad words inserted into the database!")
    else:
        print("Bad words are already loaded!")


def check_and_create_database_schema():
    conn = get_db_connection()

    cursor = conn.cursor()

    create_projects_table = '''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        code TEXT UNIQUE,
        name TEXT,
        created_at DATE DEFAULT CURRENT_TIMESTAMP
    )
    '''
    create_languages_table = '''
    CREATE TABLE IF NOT EXISTS languages (
        id INTEGER PRIMARY KEY,
        code TEXT UNIQUE,
        name TEXT,
        created_at DATE DEFAULT CURRENT_TIMESTAMP
    )
    '''

    create_bad_words_table = '''
    CREATE TABLE IF NOT EXISTS bad_words (
        id INTEGER PRIMARY KEY,
        word TEXT UNIQUE,
        total_occurrences INTEGER DEFAULT 1,
        last_occurred_at DATE DEFAULT CURRENT_TIMESTAMP,
        
        project_id INTEGER DEFAULT NULL,
        lang_id INTEGER DEFAULT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
        FOREIGN KEY (lang_id) REFERENCES languages(id)
    )
    '''

    create_phrases_table = '''
    CREATE TABLE IF NOT EXISTS bad_phrases (
        id INTEGER PRIMARY KEY,
        phrase TEXT,
        filtered_phrase TEXT,
        total_occurrences INTEGER DEFAULT 1,
        total_bad_words INTEGER DEFAULT 1,
        last_occurred_at DATE DEFAULT CURRENT_TIMESTAMP,

        project_id INTEGER DEFAULT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    '''
    create_phrase_languages_table = '''
    CREATE TABLE IF NOT EXISTS phrase_languages (
        id INTEGER PRIMARY KEY,

        phrase_id INTEGER,
        lang_id INTEGER,
        FOREIGN KEY (phrase_id) REFERENCES phrases(id),
        FOREIGN KEY (lang_id) REFERENCES languages(id)
    )
    '''

    create_bad_word_occurrences_table = '''
    CREATE TABLE IF NOT EXISTS bad_word_occurrences (
        id INTEGER PRIMARY KEY,

        phrase_id INTEGER,
        word_id INTEGER,
        FOREIGN KEY (phrase_id) REFERENCES phrases(id),
        FOREIGN KEY (word_id) REFERENCES bad_words(id)
    )
    '''

    cursor.execute(create_projects_table)
    cursor.execute(create_languages_table)
    cursor.execute(create_bad_words_table)
    cursor.execute(create_phrases_table)
    cursor.execute(create_phrase_languages_table)
    cursor.execute(create_bad_word_occurrences_table)

    conn.commit()
    conn.close()
