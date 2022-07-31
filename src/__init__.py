from flask import Flask

from src.extensions import db, ma

# from src.tasks import tasks_bp
from src.api import api_v1_bp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("src.config.DevelopmentConfig")

    register_extentions(app)

    # app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    return app


def register_extentions(app):
    db.init_app(app)
    ma.init_app(app)
