from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
from src.models.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verifica si el token está presente en el encabezado de autorización
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Formato: Bearer <token>

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decodifica el token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Busca al usuario por el ID presente en el token
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401

            # Guarda el usuario en el contexto global de la solicitud
            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated

# Middleware para requerir un token en las rutas
def require_token():
    return token_required(lambda: None)()
