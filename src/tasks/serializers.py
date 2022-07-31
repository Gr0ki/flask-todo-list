from datetime import datetime

from marshmallow import fields, post_load

from ..extensions import ma
from .models import Task


class TaskSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    notes = fields.String(required=False)
    is_done = fields.Boolean(required=False)
    updated_date_time = fields.DateTime(dump_only=True)

    class Meta:
        fields = ("id", "title", "notes", "is_done", "updated_date_time")

    @post_load
    def make_object(self, data, **kwargs):
        data["notes"] = None if "notes" not in data.keys() else data["notes"]
        data["is_done"] = False if "is_done" not in data.keys() else data["is_done"]

        return Task(
            title=data["title"],
            notes=data["notes"],
            is_done=data["is_done"],
            updated_date_time=datetime.now(),
        )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
