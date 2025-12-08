from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    with app.app_context():
        from app import views, user_routes, category_routes, record_routes
        from app import models
        
        # Register blueprints
        from app.views import bp as main_bp
        from app.currency_routes import bp as currency_bp
        from app.user_routes import bp as user_bp
        from app.category_routes import bp as category_bp
        from app.record_routes import bp as record_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(currency_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(record_bp)

    return app