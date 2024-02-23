from .config import db
from sqlalchemy.sql import func


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    bad_words = db.relationship('BadWord', back_populates='project')
    phrases = db.relationship('BadPhrase', back_populates='project')


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    bad_words = db.relationship('BadWord', back_populates='language')
    phrases = db.relationship(
        'BadPhrase', secondary='phrase_languages', back_populates='languages')


class BadWord(db.Model):
    __tablename__ = 'bad_words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), unique=True)
    total_occurrences = db.Column(db.Integer, default=1)
    last_occurred_at = db.Column(db.Date)

    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id', ondelete='SET NULL'), nullable=True)
    lang_id = db.Column(db.Integer, db.ForeignKey(
        'languages.id', ondelete='SET NULL'), nullable=True)

    project = db.relationship('Project', back_populates='bad_words')
    language = db.relationship('Language', back_populates='bad_words')
    occurrences = db.relationship(
        'BadWordOccurrence', back_populates='bad_word')


class BadPhrase(db.Model):
    __tablename__ = 'bad_phrases'

    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(2048))
    filtered_phrase = db.Column(db.String(2048))
    total_occurrences = db.Column(db.Integer, default=1)
    total_bad_words = db.Column(db.Integer, default=1)
    last_occurred_at = db.Column(db.Date)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    project = db.relationship('Project', back_populates='phrases')
    languages = db.relationship(
        'Language', secondary='phrase_languages', back_populates='phrases')
    occurrences = db.relationship('BadWordOccurrence', back_populates='phrase')


class PhraseLanguage(db.Model):
    __tablename__ = 'phrase_languages'

    id = db.Column(db.Integer, primary_key=True)

    phrase_id = db.Column(db.Integer, db.ForeignKey('bad_phrases.id'))
    lang_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    # phrase = db.relationship('BadPhrase', back_populates='languages')
    # language = db.relationship('Language', back_populates='phrases')


class BadWordOccurrence(db.Model):
    __tablename__ = 'bad_word_occurrences'

    id = db.Column(db.Integer, primary_key=True)

    phrase_id = db.Column(db.Integer, db.ForeignKey('bad_phrases.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('bad_words.id'))

    phrase = db.relationship('BadPhrase', back_populates='occurrences')
    bad_word = db.relationship('BadWord', back_populates='occurrences')
