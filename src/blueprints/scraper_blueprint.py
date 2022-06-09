import validators
from flask import Blueprint, request, jsonify
from src.database import db
from src.database.models import WebPageWordCounter
from src.utils.scrapper import main_scraper
from src.utils.custom_errors import SiteCannotBeReachedError


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

    resp = {"status": "success", "detail": "Request is processing"}
    return jsonify(resp), 200
