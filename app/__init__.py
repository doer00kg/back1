from flask import Flask

app = Flask(__name__)

from app import views

from app import user_routes

from app import category_routes

from app import record_routes
