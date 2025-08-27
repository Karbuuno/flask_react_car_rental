# server/__init__.py
import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Config
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")

    # Init extensions
    mongo.init_app(app)
    jwt.init_app(app)

    
    try:
        mongo.cx.server_info()  # Forces connection
        print("MongoDB Connected Successfully!")
    except Exception as e:
        print("MongoDB Connection Failed!")
        print(f"Error details: {e}")

    # Register blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.cars_routes import cars_bp
    app.register_blueprint(auth_bp, url_prefix="/api/users")
    app.register_blueprint(cars_bp, url_prefix="/api/cars")
    

    return app
