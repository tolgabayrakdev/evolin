from flask import Flask
import logging

from app.config import Config
from app.extensions import db
from app.middleware import register_error_handlers

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from app.routes.demo_router import demo_router

    app.register_blueprint(demo_router, url_prefix="/api/demo")

    # Initialize database (optional - app will continue if database is unavailable)
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.warning(f"Database initialization failed: {e}. App will continue without database.")

    return app
