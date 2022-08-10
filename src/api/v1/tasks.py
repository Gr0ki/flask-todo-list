from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from ...tasks.models import Task, db
from ...tasks.serializers import task_schema, tasks_schema
from .. import api_v1_tasks_bp


@api_v1_tasks_bp.route("/")
@jwt_required()
def task_list():
    user_id = get_jwt_identity()
    # get item from db
    query_result = Task.query.filter_by(user_id=user_id).all()
    if query_result == []:
        return jsonify(message="The tasks don't exist yet!"), 404
    # serialize
    serialized_result = tasks_schema.dump(query_result)
    # return json
    return jsonify(serialized_result)


@api_v1_tasks_bp.route("/new", methods=["POST"])
@jwt_required()
def create_task():
    if request.method == "POST":
        # get request data
        data = request.get_json()
        try:
            # deserialize
            deserialized_data = task_schema.load(data)
        except ValidationError as err:
            # handle deserialize exception
            return jsonify(message=err.messages), 400 if len(data) == 0 else 422
        # deserialized_data = get_deserialized_data(data, task_schema)

        # write a new task in db
        db.session.add(deserialized_data)
        db.session.commit()
        # serialize
        serialized_data = task_schema.dump(deserialized_data)
        # return json
        return jsonify(serialized_data), 201


@api_v1_tasks_bp.route("/<int:task_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def task_detailed(task_id: int):
    """RUD actions on a specific task"""
    if request.method == "GET":
        # get item from db
        query_result = Task.query.get(task_id)
        # handle 404 and 403 errors
        if query_result is None:
            return jsonify(message="That task doesn't exist!"), 404
        elif query_result.user_id != get_jwt_identity():
            return (
                jsonify(message="You have not access to this task!"),
                403,
            )
        # serialize data
        serialized_result = task_schema.dump(query_result)
        # return json
        return serialized_result

    elif request.method == "PUT":
        # get item from db
        query_result = Task.query.get(task_id)
        # handle 404 and 403 errors
        if query_result is None:
            return jsonify(message="That task doesn't exist!"), 404
        elif query_result.user_id != get_jwt_identity():
            return (
                jsonify(message="You have not access to this task!"),
                403,
            )

        # get request data
        data = request.get_json()
        # validate data
        try:
            # deserialize
            _ = task_schema.load(data)
        except ValidationError as err:
            # handle deserialize exceptions
            return jsonify(message=err.messages), 400 if len(data) == 0 else 422
        # _ = get_deserialized_data(data, task_schema)

        # update data before updating db
        if "title" in data.keys():
            query_result.title = data["title"]
        if "notes" in data.keys():
            query_result.notes = data["notes"]
        if "is_done" in data.keys():
            query_result.is_done = data["is_done"]
        # update db with updated data
        db.session.commit()
        # serialize data
        serialized_result = task_schema.dump(query_result)
        # return json
        return serialized_result, 200
        # return deserialized_result, 200

    elif request.method == "DELETE":
        # get item from db
        query_result = Task.query.get(task_id)
        # handle 404 and 403 errors
        if query_result is None:
            return jsonify(message="That task doesn't exist!"), 404
        elif query_result.user_id != get_jwt_identity():
            return (
                jsonify(message="You have not access to this task!"),
                403,
            )
        # delete from db
        db.session.delete(query_result)
        db.session.commit()
        # return json
        return jsonify(message="The task was successfuly deleted!"), 204
