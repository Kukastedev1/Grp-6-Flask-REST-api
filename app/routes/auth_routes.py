from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.utils.jwt_utils import generate_token
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)

register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = register_schema.load(request.json)
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    # Check if user exists
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({
            "status": "error",
            "message": "Username already exists"
        }), 409

    user = User(
        username=data["username"],
        role=data.get("role", "staff")
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "data": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": err.messages
        }), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    token = generate_token(user)

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200


# Example protected route (for testing RBAC)
from flask_jwt_extended import jwt_required

@auth_bp.route("/admin-only", methods=["GET"])
@jwt_required()
def admin_only():
    from app.utils.decorators import role_required

    @role_required("admin")
    def inner():
        return jsonify({
            "status": "success",
            "message": "Welcome Admin!"
        })

    return inner()