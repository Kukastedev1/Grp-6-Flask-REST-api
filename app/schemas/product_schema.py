def validate_product(data):
    required_fields = ["name", "price", "category_id", "supplier_id"]

    for field in required_fields:
        if field not in data:
            return f"{field} is required"

    if not isinstance(data.get("price"), (int, float)):
        return "Price must be a number"

    return None