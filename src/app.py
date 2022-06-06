from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


def create_app(test_config=None):
    # Instantiate application
    app = Flask(__name__, instance_relative_config=True)

    # Load application configurations
    app.config.from_object(obj="src.config.DevelopmentConfig")

    # Initialize database and instantiate migration
    from src.database import db
    from src.database.models import WebPageWordCounter

    db.init_app(app)
    migrate = Migrate(app, db)

    # CORS and CSRF
    csrf = CSRFProtect()
    csrf.init_app(app)
    CORS(app)

    # Register blueprints
    with app.app_context():
        from src.blueprints.scraper_blueprint import scraper_bp

        app.register_blueprint(scraper_bp)

    # Welcome page
    @app.get("/")
    def welcome():
        return redirect(location="https://www.google.com")

    # Page Not Found handler
    @app.errorhandler(400)
    def handle_404(e):
        return jsonify({"error": "Not found"}), 400

    # Internal Server Error handler
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Something went wrong, we are working on it"}), 500

    return app
