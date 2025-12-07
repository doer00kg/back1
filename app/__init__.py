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
        
    return app
