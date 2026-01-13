from functools import wraps
from flask import request, g
from app.utils.jwt_utils import verify_token
from app.repository.user_repository import UserRepository
from app.exceptions import AuthenticationError


def require_auth(f):
    """Decorator to require authentication for a route."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from cookie
        access_token = request.cookies.get("access_token")

        if not access_token:
            raise AuthenticationError("Authentication required", 401)

        # Verify token
        payload = verify_token(access_token)
        if not payload or payload.get("type") != "access":
            raise AuthenticationError("Invalid or expired token", 401)

        # Get user_id from payload
        user_id = payload.get("user_id")
        if not user_id or not isinstance(user_id, int):
            raise AuthenticationError("Invalid token payload", 401)

        # Get user from database
        user_repository = UserRepository()
        user = user_repository.find_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found", 401)

        # Add user to application context
        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function
