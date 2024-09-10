from flask import Blueprint
from flask import request, render_template
from src.middleware.auth_middleware import require_token
from src.controller.user_controller import (
    register,
    login,
    request_password_reset,
    reset_password,
)
from src.controller.product_controller import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)

# Create the blueprints for the routes
bp = Blueprint("routes", __name__)
user_bp = Blueprint("user_bp", __name__)
product_bp = Blueprint("product_bp", __name__)

# Add the token_required middleware to the product blueprint
product_bp.before_request(require_token)

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
@user_bp.route("/reset_password_form", methods=["GET"])
def reset_password_form():
    token = request.args.get("token")
    return render_template("reset_password_form.html", token=token)


# Routes for products
product_bp.route("/", methods=["GET"])(get_products)
product_bp.route("/create", methods=["POST"])(create_product)
product_bp.route("/get_by_id/<int:product_id>", methods=["GET"])(get_product_by_id)
product_bp.route("/update_by_id/<int:product_id>", methods=["PUT"])(update_product)
product_bp.route("/delete/<int:product_id>", methods=["DELETE"])(delete_product)
