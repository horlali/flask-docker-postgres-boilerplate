import validators
from flask import Blueprint, request, jsonify
from src.database import db
from src.database.models import WebPageWordCounter, WordCounter
from src.utils.custom_errors import SiteCannotBeReachedError
from src.utils.scrapper import main_scraper


scraper_bp = Blueprint(
    name="scraper_bp",
    import_name=__name__,
    url_prefix="/scraper",
)


@scraper_bp.route("/", methods=["GET", "POST"])
def scraper_webpage():
    url = request.get_json().get("url")

    if not validators.url(url):
        err = {
            "status": "failed",
            "detail": "Invalid url! Use format eg `https://www.example.com",
        }
        return jsonify(err), 400

    if url is None:
        err = {"status": "failed", "detail": "KeyError [url]"}
        return jsonify(err), 400

    try:
        word_count_json = main_scraper(url=url)
        results = WebPageWordCounter(url=url, word_count_json=word_count_json)
        db.session.add(results)
        db.session.commit()
    except SiteCannotBeReachedError:
        err = {"status": "failed", "detail": "The url you submitted cannot be reached"}
        return jsonify(err), 400

    resp = {"status": "success", "data": word_count_json}
    return jsonify(resp), 200


def inject_into_db(parsered_dict: str):

    injection_set = [
        WordCounter(salted_hash=key, encrypted_word=value[0], frequency=value[1])
        for key, value in parsered_dict.items()
    ]

    print(injection_set[:10])
    db.session.bulk_save_objects(injection_set)
    db.session.commit()


# inject_into_db(main_scraper(url="https://bbc.com"))
