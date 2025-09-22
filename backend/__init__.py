# server/__init__.py
import os

import cloudinary
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # Config
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")

    # Init extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # Cloudinary Config
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    try:
        mongo.cx.server_info()  # Forces connection
        print("MongoDB Connected Successfully!")
    except Exception as e:
        print("MongoDB Connection Failed!")
        print(f"Error details: {e}")

    # Register blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.bookings_routes import bookings_bp
    from backend.routes.cars_routes import cars_bp
    from backend.routes.stripe_routes import stripe_bp

    app.register_blueprint(auth_bp, url_prefix="/api/users")
    app.register_blueprint(cars_bp, url_prefix="/api/cars")
    app.register_blueprint(stripe_bp, url_prefix="/api/stripe")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")

    return app
