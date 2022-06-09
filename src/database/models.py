from sqlalchemy.dialects.postgresql import JSON
from src.database import db


class WebPageWordCounter(db.Model):
    __tablename__ = "Website_Word_Counter"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    word_count_json = db.Column(JSON)
    # result_no_stop_words = db.Column(JSON)

    def __init__(self, url, word_count_json):
        self.url = url
        self.word_count_json = word_count_json
        # self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return f"id {self.id}"
