from flask import Blueprint, jsonify, request, make_response, g
from app.service.auth_service import AuthService
from app.middleware import require_auth


auth_router = Blueprint("auth", __name__)
auth_service = AuthService()


@auth_router.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    auth_service.register(data)

    return jsonify({"message": "User registered successfully"}), 201


@auth_router.route("/login", methods=["POST"])
def login():
    """Login user and set tokens as httpOnly cookies."""
    data = request.get_json()
    result = auth_service.login(data.get("email"), data.get("password"))

    response = make_response(jsonify({"message": "Login successful"}))
    
    # Set httpOnly cookies
    response.set_cookie(
        "access_token",
        result["access_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        max_age=3600,  # 1 hour
    )
    response.set_cookie(
        "refresh_token",
        result["refresh_token"],
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        max_age=604800,  # 7 days
    )

    return response, 200


@auth_router.route("/logout", methods=["POST"])
@require_auth
def logout():
    """Logout user by clearing cookies."""
    response = make_response(jsonify({"message": "Logout successful"}))
    
    # Clear cookies
    response.set_cookie("access_token", "", httponly=True, max_age=0)
    response.set_cookie("refresh_token", "", httponly=True, max_age=0)

    return response, 200


@auth_router.route("/me", methods=["GET"])
@require_auth
def me():
    """Get current authenticated user information."""
    user = g.current_user
    return jsonify(user.to_dict()), 200