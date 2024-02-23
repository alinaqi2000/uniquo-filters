from flask import Blueprint, request
from services.requests import ok_response
from filters.main import filter_bad_words

filter_bad_text = Blueprint('filter_bad_text', __name__)


@filter_bad_text.route('/filter-bad-words', methods=["POST"])
def filter_bad_phrase():
    request_body = request.get_json()

    if (request_body.get('text') == None or request_body.get('text') == ""):
        return ok_response({"error": "Please add valid data"})

    phrase, total_words, bad_words_language = filter_bad_words(
        request_body.get('text'))

    return ok_response({"processed_text": phrase, "bad_words": total_words, "bad_words_language": bad_words_language})
