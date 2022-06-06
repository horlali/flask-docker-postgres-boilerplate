from flask import Blueprint, request, jsonify


scraper_bp = Blueprint(
    name="scraper_bp",
    import_name=__name__,
    url_prefix="/scraper",
)


@scraper_bp.route("/", methods=["GET", "POST"])
def scraper_webpage():

    resp = {"status": "success", "detail": "Request is processing"}
    return jsonify(resp), 200
