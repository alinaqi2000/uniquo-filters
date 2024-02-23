from services.words import list_bad_words
from services.projects import get_single_project_by_id
from services.languages import get_single_language_by_id


def bad_words_resource(condition=(), with_details=True):
    data = []
    bad_words = list_bad_words(condition)
    for word in bad_words:
        prepared_word = {
            "id": word.id,
            "word": word.word,
            "total_occurrences": word.total_occurrences,
            "last_occurred_at": word.last_occurred_at,
        }

        if with_details:
            project = get_single_project_by_id(word.project_id)
            if project is not None:
                prepared_word["project"] = {
                    "id": project.id, "code": project.code, "name": project.name}

            lang = get_single_language_by_id(word.lang_id)
            if lang is not None:
                prepared_word["language"] = {
                    "id": lang.id, "code": lang.code, "name": lang.name}

        data.append(prepared_word)
    return data
