from datetime import datetime

from flask_jwt_extended import get_jwt_identity
from marshmallow import fields, post_load

from ..extensions import ma
from .models import Task


class TaskSchema(ma.Schema):

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    updated_date_time = fields.DateTime(dump_only=True)
    title = fields.String(required=True)
    notes = fields.String(required=False)
    is_done = fields.Boolean(required=False)

    class Meta:
        fields = ("id", "title", "notes", "is_done", "updated_date_time")

    @post_load
    def make_object(self, data, **kwargs):
        data["notes"] = None if "notes" not in data.keys() else data["notes"]
        data["is_done"] = False if "is_done" not in data.keys() else data["is_done"]
        data["updated_date_time"] = datetime.now()
        data["user_id"] = get_jwt_identity()
        return Task(**data)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
