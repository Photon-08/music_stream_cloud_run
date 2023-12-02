import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(base_dir,"../db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR,"myappdb.sqlite3")
    UPLOAD_FOLDER = "static/musics/"