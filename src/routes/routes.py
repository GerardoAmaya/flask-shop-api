from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    return "Welcome to Sportify!"
