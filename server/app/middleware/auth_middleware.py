from functools import wraps
from flask import request, g
import logging
from app.utils.jwt_utils import verify_token
from app.repository.user_repository import UserRepository
from app.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


def require_auth(f):
    """Decorator to require authentication for a route."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from cookie
        access_token = request.cookies.get("access_token")

        if not access_token:
            logger.warning("No access token found in cookies")
            raise AuthenticationError("Authentication required", 401)

        # Verify token
        payload = verify_token(access_token)
        if not payload:
            logger.warning("Token verification failed or token expired")
            raise AuthenticationError("Invalid or expired token", 401)

        if payload.get("type") != "access":
            logger.warning(f"Invalid token type: {payload.get('type')}")
            raise AuthenticationError("Invalid token type", 401)

        # Get user_id from payload
        user_id = payload.get("user_id")
        if not user_id or not isinstance(user_id, int):
            logger.warning(f"Invalid user_id in token: {user_id}")
            raise AuthenticationError("Invalid token payload", 401)

        # Get user from database
        user_repository = UserRepository()
        user = user_repository.find_by_id(user_id)
        if not user:
            logger.warning(f"User not found for user_id: {user_id}")
            raise AuthenticationError("User not found", 401)

        # Add user to application context
        g.current_user = user

        return f(*args, **kwargs)

    return decorated_function
