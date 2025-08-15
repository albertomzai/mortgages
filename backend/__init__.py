from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

_db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hipotecas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    _db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar blueprint de la API
    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    with app.app_context():
        _db.create_all()

    return app