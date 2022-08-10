from flask import jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError


from ...auth.models import User, db
from ...auth.serializers import user_schema
from .. import api_v1_auth_bp


@api_v1_auth_bp.route("/register", methods=["POST"])
def register():
    # take data for registration
    data = request.get_json()
    try:
        # deserialize
        deserialized_data = user_schema.load(data)
    except ValidationError as err:
        # handle deserialize exception
        return jsonify(message=err.messages), 400 if len(data) == 0 else 422
    # check if email is taken
    test = User.query.filter_by(email=deserialized_data.email).first()
    if test != None:
        # return error
        return jsonify(message="That user is already exists."), 409
    else:
        # add username creation from email
        user = User(email=deserialized_data.email, password=deserialized_data.password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfuly."), 201


@api_v1_auth_bp.route("/login", methods=["POST"])
def login():
    # take login data
    email = request.json["email"]
    password = request.json["password"]

    # check if login data match any user in the db
    test = User.query.filter_by(email=email, password=password).first()
    if test == None:
        # return error
        return jsonify(message="Wrong login or password."), 401
    else:
        # return success message and JWT success token
        access_token = create_access_token(identity=test.id)
        return jsonify(message="Login succeeded.", access_token=access_token), 200
