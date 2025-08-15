import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Load configuration from environment or defaults
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///hipotecas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # Serve the frontend index.html at root
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    return app