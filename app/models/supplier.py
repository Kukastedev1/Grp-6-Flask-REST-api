from app import db

class Supplier(db.Model):
    """
    Handles vendor information and contact details for sourcing products.
    """
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    contact_person = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    # Relationships
    products = db.relationship('Product', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_person": self.contact_person,
            "email": self.email,
            "phone": self.phone
        }