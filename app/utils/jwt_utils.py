from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_token(user):
    return create_access_token(
        identity={
            "id": user.id,
            "role": user.role
        },
        expires_delta=timedelta(hours=2)
    )