from flask import Blueprint
from resources.bad_word import bad_words_resource
from services.requests import ok_response

bad_words = Blueprint('bad_words', __name__)


@bad_words.route('/bad-words')
def bad_words_list():
    words = bad_words_resource()
    return ok_response({"total": len(words), 'words': words})
