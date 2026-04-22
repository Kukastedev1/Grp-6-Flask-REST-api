from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, validate=validate.Length(min=4))
    role = fields.String(validate=validate.OneOf(["admin", "manager", "staff"]))


class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)