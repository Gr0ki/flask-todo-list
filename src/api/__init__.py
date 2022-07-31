from flask import Blueprint

api_v1_bp = Blueprint("api/v1", __name__, url_prefix="/api/v1")

from .v1.views import *
