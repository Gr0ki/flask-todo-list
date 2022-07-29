from ..extensions import ma


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "notes", "is_done", "updated_date_time")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
