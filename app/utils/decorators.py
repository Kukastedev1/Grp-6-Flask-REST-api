from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user = get_jwt_identity()

            if user["role"] != required_role:
                return jsonify({
                    "status": "error",
                    "message": "Access denied: insufficient permissions"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper