import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Database constants
DB_HOST: int = os.environ.get("DB_HOST")
DB_PORT: str = os.environ.get("DB_PORT")
DB_NAME: str = os.environ.get("DB_NAME")
DB_USERNAME: str = os.environ.get("DB_USERNAME")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
DB_URI: str = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URI = "sqlite:///db.sqlite3"


# Configurations
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
