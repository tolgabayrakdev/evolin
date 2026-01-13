import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from flask import current_app


def generate_access_token(user_id: int, email: str) -> str:
    """Generate JWT access token."""
    payload = {
        "user_id": user_id,
        "email": email,
        "type": "access",
        "exp": datetime.now() + timedelta(hours=1),
        "iat": datetime.now(),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def generate_refresh_token(user_id: int, email: str) -> str:
    """Generate JWT refresh token."""
    payload = {
        "user_id": user_id,
        "email": email,
        "type": "refresh",
        "exp": datetime.now() + timedelta(days=7),
        "iat": datetime.now(),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
