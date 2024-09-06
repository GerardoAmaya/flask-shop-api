from flask import request, jsonify, current_app, render_template
from src.db import db
from src.models.models import User
from src.validators.user_validator import (
    UserRegisterSchema,
    UserLoginSchema,
    PasswordResetRequestSchema,
    ResetPasswordSchema,
)
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from src.helpers.http_helper import HttpHelper
from datetime import datetime, timedelta
from extensions import mail


def register():
    """
    Register a new user in the system.

    This function validates the user input, hashes the password,
    and saves the user in the database.

    Returns:
        JSON response with success or error message.
    """
    schema = UserRegisterSchema()

    try:
        # Validate the incoming JSON data using the schema
        user_data = schema.load(request.json)

        # Hash the user's password
        hashed_password = generate_password_hash(user_data["password"])

        # Create a new user instance
        new_user = User(
            email=user_data["email"],
            password=hashed_password,
            role_id=user_data["role_id"],
        )

        # Add the user to the database and commit the transaction
        db.session.add(new_user)
        db.session.commit()

        # Return success response
        return HttpHelper.response(
            HttpHelper.retCreated, {"message": "User successfully registered"}
        )

    except ValidationError as err:
        db.session.rollback()  # Rollback if validation fails
        return HttpHelper.response(HttpHelper.retUnprocessableContent, err.messages)

    except Exception as e:
        db.session.rollback()  # Rollback for any other exception
        return HttpHelper.response(HttpHelper.retErrorServer, str(e))

    finally:
        db.session.close()  # Close the session in any case


def login():
    """
    Handle user login.

    This function checks user credentials and returns an appropriate response.

    Returns:
        JSON response with success or error message.
    """
    schema = UserLoginSchema()

    try:
        # Validate the incoming JSON data
        login_data = schema.load(request.json)

        # Find the user by email
        user = User.query.filter_by(email=login_data["email"]).first()

        if not user:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "User not found"}
            )

        # Check if the password matches
        if not check_password_hash(user.password, login_data["password"]):
            return HttpHelper.response(
                HttpHelper.retUnauthorized, {"message": "Incorrect password"}
            )

        # Return success response (could return token, JWT, etc.)
        return HttpHelper.response(HttpHelper.retOK, {"message": "Login successful"})

    except ValidationError as err:
        return HttpHelper.response(HttpHelper.retUnprocessableContent, err.messages)

    except Exception as e:
        return HttpHelper.response(HttpHelper.retErrorServer, str(e))


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset-salt")


def request_password_reset():
    """
    Request a password reset token for a user.

    The token is sent to the user's email address if the user exists.

    Returns:
        JSON response with success or error message.
    """
    schema = PasswordResetRequestSchema()

    try:
        # Validate the request data
        user_data = schema.load(request.json)

        email = user_data["email"]

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if not user:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "User not found"}
            )

        # Generate token
        token = generate_reset_token(user.email)

        # Update the user with the reset token and expiry date
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(
            hours=1
        )  # Token valid for 1 hour

        # Commit the changes to the database
        db.session.commit()

        # Generate the reset URL
        reset_url = f"http://localhost:5000/user/reset_password_form?token={token}"

        # Render the email template and pass the reset URL to the template
        html_body = render_template("reset_password.html", reset_url=reset_url)

        # Send the token via email
        msg = Message("Password Reset Request", recipients=[user.email])
        msg.html = html_body  # Use HTML body for the email

        # Send the email
        mail.send(msg)

        return HttpHelper.response(
            HttpHelper.retOK, {"message": "Password reset token sent to your email"}
        )

    except ValidationError as err:
        return HttpHelper.response(HttpHelper.retError, err.messages)

    except Exception as e:
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})


def verify_reset_token(token):
    """
    Verify the password reset token.

    Args:
        token (str): The reset token to verify.

    Returns:
        str: The email associated with the token if valid, otherwise None.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt="password-reset-salt", max_age=3600
        )  # Token valid for 1 hour
        return email
    except SignatureExpired:
        return None  # Token expired
    except BadSignature:
        return None  # Invalid token


def reset_password():
    """
    Reset the user's password using a valid reset token.

    The token must be valid and the user must exist for the password to be reset.

    Returns:
        JSON response with success or error message.
    """
    schema = ResetPasswordSchema()

    try:
        # Validate the incoming JSON data
        reset_data = schema.load(request.json)

        token = reset_data["token"]
        new_password = reset_data["new_password"]

        # Verify the token
        email = verify_reset_token(token)
        if not email:
            return HttpHelper.response(
                HttpHelper.retError, {"message": "Invalid or expired token"}
            )

        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "User not found"}
            )

        # Update the user's password
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password

        # Commit the changes
        db.session.commit()

        return HttpHelper.response(
            HttpHelper.retOK, {"message": "Password successfully reset"}
        )

    except ValidationError as err:
        return HttpHelper.response(HttpHelper.retUnprocessableContent, err.messages)

    except Exception as e:
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})
