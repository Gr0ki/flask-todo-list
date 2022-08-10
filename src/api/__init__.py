from flask import Blueprint

api_v1_tasks_bp = Blueprint("api/v1/tasks", __name__, url_prefix="/api/v1/tasks")
api_v1_auth_bp = Blueprint("api/v1/auth", __name__, url_prefix="/api/v1/auth")

from .v1.tasks import *
from .v1.auth import *
