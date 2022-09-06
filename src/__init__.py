from flask import Flask

from src.api import api_v1_auth_bp, api_v1_tasks_bp
from src.extensions import db, jwt, ma


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("src.config.ProductionConfig")

    register_extentions(app)

    app.register_blueprint(api_v1_tasks_bp, url_prefix="/api/v1/tasks")
    app.register_blueprint(api_v1_auth_bp, url_prefix="/api/v1/auth")

    return app


def register_extentions(app):
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
