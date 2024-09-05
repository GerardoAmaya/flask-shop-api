from flask import request, jsonify, current_app
from src.db import db
from src.models.models import User
from src.validators.user_validator import UserRegisterSchema, UserLoginSchema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from src.helpers.http_helper import HttpHelper
from datetime import datetime, timedelta


# Register a new user with transaction handling
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


# User login
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
    email = request.json.get("email")

    if not email:
        return HttpHelper.response(
            HttpHelper.retError, {"message": "Email is required"}
        )

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

    # Send the token via email
    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = f"Your password reset token is: {token}"

    # TODO: Send the email template with the token
    # mail.send(msg)

    return HttpHelper.response(
        HttpHelper.retOK, {"message": "Password reset token sent to your email"}
    )


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


# Reset the password using the token
def reset_password():
    """
    Reset the user's password using a valid reset token.

    The token must be valid and the user must exist for the password to be reset.

    Returns:
        JSON response with success or error message.
    """
    token = request.json.get("token")
    new_password = request.json.get("new_password")

    if not token or not new_password:
        return HttpHelper.response(
            HttpHelper.retError, {"message": "Token and new password are required"}
        )

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
