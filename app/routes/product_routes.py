from flask import Blueprint, request, jsonify
from app.models.product import Product, db
from schemas.product_schema import validate_product

product_bp = Blueprint('products', __name__)

# CREATE
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    error = validate_product(data)
    if error:
        return jsonify({"error": error}), 400

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data.get("stock", 0),
        category_id=data["category_id"],
        supplier_id=data["supplier_id"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


# READ ALL
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200


# READ ONE
@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


# UPDATE
@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.category_id = data.get("category_id", product.category_id)
    product.supplier_id = data.get("supplier_id", product.supplier_id)

    db.session.commit()

    return jsonify(product.to_dict()), 200


# DELETE
@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200