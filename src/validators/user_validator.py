# src/validators/user_validator.py
from marshmallow import Schema, fields, validate, ValidationError


class UserRegisterSchema(Schema):
    """
    This class is a schema validator for the user registration endpoint.
    It validates the incoming JSON data for registering a new
    user in the system.
    """

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
    """
    This class is a schema validator for the user login endpoint.
    It validates the incoming JSON data for logging in a user.
    """

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


class PasswordResetRequestSchema(Schema):
    """
    This class is a schema validator for the password reset request endpoint.
    It validates the incoming JSON data for requesting a password reset.
    """

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format.",
        },
    )


class ResetPasswordSchema(Schema):
    """
    This class is a schema validator for the password reset endpoint.
    It validates the incoming JSON data for resetting the password.
    """

    token = fields.Str(
        required=True,
        error_messages={
            "required": "Token is required.",
        },
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            "required": "New password is required.",
            "min": "Password must be at least 6 characters long.",
        },
    )
