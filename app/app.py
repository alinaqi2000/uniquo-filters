from flask import Flask, jsonify, request, send_file
from filters.main import google_perspective_score, filter_bad_words
from db.setup_database import check_and_create_database_schema, load_words_into_database
from services.words import list_bad_words
from services.utils import generate_public_key
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

check_and_create_database_schema()
load_words_into_database()


@app.before_request
def check_token():
    if request.path != "/give-me-public-encryption-key":
        print(request.path)


@app.route('/')
def hello():
    return jsonify({'message': 'Ali Naqi Al-Musawi is here!'})


@app.route('/give-me-public-encryption-key')
def encryption_key():
    return send_file(generate_public_key(), as_attachment=True)


@app.route('/bad-words')
def bad_words_list():
    rows = list_bad_words()
    return jsonify({"total": len(rows), 'words': [dict(row) for row in rows]})


@app.route('/google-perspective', methods=["POST"])
def google_perspective():
    request_body = request.get_json()
    if (request_body.get('text') == None or request_body.get('text') == ""):
        return jsonify({"error": "Please add valid data"})

    return jsonify({"success": google_perspective_score(request_body.get('text'))})


@app.route('/filter-bad-word', methods=["POST"])
def bad_word():
    request_body = request.get_json()
    if (request_body.get('text') == None or request_body.get('text') == ""):
        return jsonify({"error": "Please add valid data"})

    return jsonify({"success": filter_bad_words(request_body.get('text'))})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
