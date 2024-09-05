# src/validators/user_validator.py
from marshmallow import Schema, fields, validate, ValidationError


class UserRegisterSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format.",
        },
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            "required": "Password is required.",
            "min": "Password must be at least 6 characters long.",
        },
    )

    role_id = fields.Integer(
        required=True, error_messages={"required": "Role ID is required."}
    )


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format.",
        },
    )

    password = fields.Str(
        required=True, error_messages={"required": "Password is required."}
    )
