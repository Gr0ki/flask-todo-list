import re
from datetime import datetime

from marshmallow import ValidationError, fields, post_load, validates

from ..extensions import ma
from .models import User


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=False)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    last_login = fields.DateTime(dump_only=True)

    @validates("password")
    def validates_password(seld, value):
        if len(value) < 6:
            raise ValidationError("Password length must be longer then 5.")
        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain at least 1 upper case letter.")
        if not any(c.islower() for c in value):
            raise ValidationError("Password must contain at least 1 lower case letter.")
        if not any(c.isdecimal() for c in value):
            raise ValidationError(
                "Password must contain at least 1 decimal digit (0-9)."
            )

    @validates("email")
    def validates_email(seld, value):
        if not re.match("[^^]+@[^@]+\.[^@]+", value):
            # [^^]+ - 1 or more of any symbol exept "^"
            # [^@]+ - 1 or more of any symbol exept "@"
            # \. - "."
            # @ - "@"
            raise ma.ValidationError("Invalid email format.")

    @post_load
    def process_input(self, data, **kwargs):
        data["last_login"] = datetime.now()
        data["email"] = data["email"].lower().strip()
        data["password"] = data["password"]  # TODO: add hashing

        if "username" not in data.keys() and "email" in data.keys():
            data["username"] = data["email"][: data["email"].find("@")]

        return User(**data)


user_schema = UserSchema()