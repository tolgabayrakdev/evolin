from flask import Flask, jsonify
from app.exceptions import BaseAppException


def register_error_handlers(app: Flask):
    """Register global error handlers for the Flask application."""
    
    @app.errorhandler(BaseAppException)
    def handle_app_exception(e: BaseAppException):
        return jsonify(e.to_dict()), e.status_code
    
    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        error = BaseAppException(str(e), 400, "Validation error occurred")
        return jsonify(error.to_dict()), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        error = BaseAppException("Resource not found", 404)
        return jsonify(error.to_dict()), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        error = BaseAppException("Internal server error", 500)
        return jsonify(error.to_dict()), 500
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        message = str(e) if str(e) else "An unexpected error occurred"
        error = BaseAppException(message, 500)
        return jsonify(error.to_dict()), 500
