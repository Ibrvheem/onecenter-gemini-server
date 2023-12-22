from flask import jsonify, request, g
from app import app
import jwt

from functools import wraps

from app.platform.model import Platform
from app.user.model import User


def auth_required(*roles_required):
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Missing Authorization Header"}), 401
            try:
                token = auth_header.split(' ')[1]
                payload = jwt.decode(token, app.config.get('JWT_SECRET_KEY'), algorithms=["HS256"])
                auth_id = payload['sub']
                role = payload['role']
                # check role
                if roles_required:
                    if role not in roles_required:
                        return jsonify({"message": "Unauthorized to perform action"}), 401
            except Exception as e:
                return jsonify({"message": "Unauthorized to perform action"}), 401
            g.user = User.get_by_id(auth_id)
            return f(*args, **kwargs)
        return decorated
    return requires_auth

def platform_auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not (auth and Platform.is_authorized(auth.username, auth.password)):
                return jsonify({"message": "Missing Authorization Header"}), 401
            g.platform = Platform.get_by_username(auth.username)
            return f(*args, **kwargs)
        return decorated
    