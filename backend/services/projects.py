from db.models import Project
from db.config import db


def get_single_project(project_code):
    return db.session.query(Project).filter_by(code=project_code).first()


def get_single_project_by_id(project_id):
    return db.session.query(Project).filter_by(id=project_id).first()


def list_projects():
    return db.session.query(Project).all()


def count_projects(condition=()):
    return db.session.query(Project).filter(*condition).count()


def project_exists(code: str) -> bool:
    return db.session.query(Project).filter_by(code=code).count() > 0


def insert_project(code: str, name: str):
    project = Project(code=code, name=name)
    db.session.add(project)
    db.session.commit()

    return project
