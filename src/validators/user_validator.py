# src/validators/user_validator.py
from marshmallow import Schema, fields, validate, ValidationError


# Validator for user registration
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


# Validator for user login
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


# Validator for password reset request
class PasswordResetRequestSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format.",
        },
    )

# Validator for confirming the password reset, and setting a new password
class ResetPasswordSchema(Schema):
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
