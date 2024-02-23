from services.phrases import list_bad_phrases, get_phrase_languages
from services.projects import get_single_project
from services.languages import get_single_language


def bad_phrases_resource(condition=(), with_details=True):
    data = []
    bad_phrases = list_bad_phrases(condition)
    for phrase in bad_phrases:
        prepared_phrase = {
            "id": phrase["id"],
            "phrase": phrase["phrase"],
            "filtered_phrase": phrase["filtered_phrase"],
            "total_occurrences": phrase["total_occurrences"],
            "total_bad_words": phrase["total_bad_words"],
            "last_occurred_at": phrase["last_occurred_at"],
        }

        if with_details:
            project = get_single_project(("id", phrase['project_id']))
            if project is not None:
                prepared_phrase["project"] = {
                    "id": project['id'], "code": project['code'], "name": project['name']}

            languages = get_phrase_languages(prepared_phrase["id"])
            prepared_phrase["languages"] = []
            if languages is not None:
                for lang in languages:
                    prepared_phrase["languages"].append({
                        "id": lang['id'], "code": lang['code'], "name": lang['name']})

        data.append(prepared_phrase)
    return data
