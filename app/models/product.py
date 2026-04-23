from app import db
from datetime import datetime
from app.models.supplier import product_suppliers


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", back_populates="products")

    suppliers = db.relationship(
        "Supplier",
        secondary=product_suppliers,
        back_populates="products",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at,
            "category_id": self.category_id,
            "category": self.category.name if self.category else None,
            "suppliers": [s.name for s in self.suppliers],
        }
