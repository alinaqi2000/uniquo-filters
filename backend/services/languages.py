from sqlalchemy import func
from db.models import Language
from db.config import db


def get_single_language(lang_code):
    return db.session.query(Language).filter_by(code=lang_code).first()


def get_single_language_by_id(lang_id):
    return db.session.query(Language).filter_by(id=lang_id).first()


def list_languages():
    return Language.query.all()


def count_languages(condition=()):
    return Language.query.filter(*condition).count()


def language_exists(code: str) -> bool:
    return Language.query.filter_by(code=code).count() > 0


def insert_language(code: str, name: str):
    language = Language(code=code, name=name)
    db.session.add(language)
    db.session.commit()

    return language
