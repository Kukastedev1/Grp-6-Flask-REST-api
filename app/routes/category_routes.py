from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

category_bp = Blueprint("category_bp", __name__)

@category_bp.route("/", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200

@category_bp.route("/", methods=["POST"])
def create_category():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    if Category.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(
        name=data["name"],
        description=data.get("description"),
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()

    if "name" in data:
        existing = Category.query.filter_by(name=data["name"]).first()
        if existing and existing.id != category_id:
            return jsonify({"error": "Category name already taken"}), 409
        category.name = data["name"]

    if "description" in data:
        category.description = data["description"]

    db.session.commit()
    return jsonify(category.to_dict()), 200

@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": f"Category '{category.name}' deleted successfully"}), 200
