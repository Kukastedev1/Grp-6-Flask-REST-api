from flask import Blueprint, request, jsonify
from app import db
from app.models.supplier import Supplier
from app.models.product import Product

supplier_bp = Blueprint("supplier_bp", __name__)

@supplier_bp.route("/", methods=["GET"])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([s.to_dict() for s in suppliers]), 200

@supplier_bp.route("/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify(supplier.to_dict()), 200

@supplier_bp.route("/", methods=["POST"])
def create_supplier():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "Supplier name is required"}), 400

    if Supplier.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Supplier already exists"}), 409

    supplier = Supplier(
        name=data["name"],
        contact_name=data.get("contact_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address"),
    )
    db.session.add(supplier)
    db.session.commit()
    return jsonify(supplier.to_dict()), 201

@supplier_bp.route("/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()

    if "name" in data:
        existing = Supplier.query.filter_by(name=data["name"]).first()
        if existing and existing.id != supplier_id:
            return jsonify({"error": "Supplier name already taken"}), 409
        supplier.name = data["name"]

    for field in ["contact_name", "email", "phone", "address"]:
        if field in data:
            setattr(supplier, field, data[field])

    db.session.commit()
    return jsonify(supplier.to_dict()), 200

@supplier_bp.route("/<int:supplier_id>", methods=["DELETE"])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": f"Supplier '{supplier.name}' deleted successfully"}), 200

@supplier_bp.route("/<int:supplier_id>/products/<int:product_id>", methods=["POST"])
def assign_product(supplier_id, product_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    product = Product.query.get_or_404(product_id)

    if product in supplier.products:
        return jsonify({"message": "Product already linked to this supplier"}), 409

    supplier.products.append(product)
    db.session.commit()
    return jsonify({"message": f"Product '{product.name}' linked to supplier '{supplier.name}'"}), 200

@supplier_bp.route("/<int:supplier_id>/products/<int:product_id>", methods=["DELETE"])
def remove_product(supplier_id, product_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    product = Product.query.get_or_404(product_id)

    if product not in supplier.products:
        return jsonify({"error": "Product not linked to this supplier"}), 404

    supplier.products.remove(product)
    db.session.commit()
    return jsonify({"message": f"Product '{product.name}' unlinked from supplier '{supplier.name}'"}), 200
