from flask import Blueprint
from resources.bad_phrases import bad_phrases_resource
from services.requests import ok_response

bad_phrases = Blueprint('bad_phrases', __name__)


@bad_phrases.route('/bad-phrases')
def bad_phrases_list():
    phrases = bad_phrases_resource()
    return ok_response({"total": len(phrases), 'phrases': phrases})
