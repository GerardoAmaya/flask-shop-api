from flask import Blueprint
from src.controller.user_controller import register, login, request_password_reset, reset_password
from flask import request, render_template

bp = Blueprint("routes", __name__)
user_bp = Blueprint("user_bp", __name__)


@bp.route("/")
def home():
    return "Welcome to Sportify!"


# User registration
user_bp.route("/register", methods=["POST"])(register)

# User login
user_bp.route("/login", methods=["POST"])(login)

# Request password reset token
user_bp.route("/request_password_reset", methods=["POST"])(request_password_reset)

# Reset password with the token
user_bp.route("/reset_password", methods=["POST"])(reset_password)

# Reset password form with the token in the URL query parameter
@user_bp.route('/reset_password_form', methods=['GET'])
def reset_password_form():
    token = request.args.get("token")
    return render_template("reset_password_form.html", token=token)