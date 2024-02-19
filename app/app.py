from flask import Flask, request, send_file
from filters.main import google_perspective_score
from db.setup_database import check_and_create_database_schema, seed_database
from services.utils import generate_public_key, env
from services.requests import ok_response
from services.projects import project_exists, get_single_project
from dotenv import load_dotenv
from routes.bad_words import bad_words
from routes.bad_phrases import bad_phrases
from routes.filter_bad_text import filter_bad_text

# load environment variables from .env
load_dotenv()

# database setup
check_and_create_database_schema()
seed_database()

app = Flask(__name__)

app.register_blueprint(bad_words)
app.register_blueprint(bad_phrases)
app.register_blueprint(filter_bad_text)


@app.before_request
def check_token():
    if request.path != "/give-me-public-encryption-key":
        app.config['public_key'] = request.headers["Public-Access-Key"]
        app.config['project_code'] = request.headers["Project-Code"]

        if not app.config['public_key']:
            return ok_response({"error": "Please add a valid public access key."}, 401)

        if not app.config['project_code'] or not project_exists(app.config['project_code']):
            return ok_response({"error": "Please add a valid project code"}, 401)
        project = get_single_project(("code", app.config['project_code']))
        if project != None:
            app.config['project_id'] = project["id"]


@app.route('/')
def hello():
    return ok_response({'api': 'Uniquo - Bad Words Filter API', 'author': "Ali Naqi Al-Musawi!"})


@app.route('/give-me-public-encryption-key')
def encryption_key():
    return send_file(generate_public_key(), as_attachment=True)


@app.route('/google-perspective', methods=["POST"])
def google_perspective():
    request_body = request.get_json()
    if (request_body.get('text') == None or request_body.get('text') == ""):
        return ok_response({"error": "Please add valid data"})

    return ok_response({"success": google_perspective_score(request_body.get('text'))})


if __name__ == '__main__':
    match env("APP_MODE"):
        case "production":
            from waitress import serve
            serve(app, host="0.0.0.0", port=5000)
        case _:
            app.run(host='0.0.0.0', port=5000, debug=True)
