from flask import jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from ...auth.models import User, db
from ...auth.serializers import register_user_schema, user_schema
from .. import api_v1_auth_bp


@api_v1_auth_bp.route("/register", methods=["POST"])
def register():
    # TODO: check for errors
    # take data for registration
    data = request.get_json()
    try:
        # deserialize
        deserialized_data = register_user_schema.load(data)
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
        user = User(email=deserialized_data.email)
        user.password_hash = generate_password_hash(deserialized_data.password_hash)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfuly."), 201


@api_v1_auth_bp.route("/login", methods=["POST"])
def login():
    # TODO: check for errors
    # take login data
    data = request.get_json()
    try:
        # deserialize
        deserialized_data = user_schema.load(data)
        password = deserialized_data.password_hash
        email = deserialized_data.email
        last_login = deserialized_data.last_login
    except ValidationError as err:
        # handle deserialize exception
        return jsonify(message=err.messages), 400 if len(data) == 0 else 422

    # check if login data match any user in the db or is is a user password valid
    user = User.query.filter_by(email=email).first()
    if user == None or not user.verify_password(password):
        # return error
        return jsonify(message="Wrong login or password."), 401
    else:
        # return success message and JWT success token
        access_token = create_access_token(identity=user.id)
        user.last_login = last_login
        db.session.commit()
        return jsonify(message="Login succeeded.", access_token=access_token), 200
