from flask_sqlalchemy import SQLAlchemy
from services.utils import env

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    # with app.app_context():
        # db.drop_all()
        # db.create_all()
