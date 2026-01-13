from flask import Flask

from app.config import Config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    # Register blueprints
    from app.routes.demo_router import demo_router
    
    app.register_blueprint(demo_router, url_prefix='/api/demo')
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app