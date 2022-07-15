import os
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import EncryptedType
from src.database import db


_ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")


class WebPageWordCounter(db.Model):
    __tablename__ = "Website_Word_Counter"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    word_count_json = db.Column(JSON)

    def __init__(self, url, word_count_json):
        self.url = url
        self.word_count_json = word_count_json

    def __repr__(self):
        return f"id {self.id}"


class WordCounter(db.Model):
    __tablename__ = "word_counter"

    id = db.Column(db.Integer)
    salted_hash = db.Column(db.String(), primary_key=True)
    encrypted_word = db.Column(EncryptedType(db.String, _ENCRYPTION_KEY))
    frequency = db.Column(db.Integer)

    def __init__(self, salted_hash, encrypted_word, frequency):
        self.salted_hash = salted_hash
        self.encrypted_word = encrypted_word
        self.frequency = frequency
