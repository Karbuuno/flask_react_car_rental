from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from server import mongo 
from server.utils.jwt import generate_token, decode_token

from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# Mongo collection
users = mongo.db.users


# ----------------------------
# @desc    Auth user & get token
# @route   POST /api/users/auth
# @access  Public
# ----------------------------
@auth_bp.route("/auth", methods=["POST"])
def auth_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            payload = {
                "user_id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "isAdmin": user.get("isAdmin", False),
            }
            return generate_token(user,payload)

        return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# @desc    Register new user
# @route   POST /api/users
# @access  Public
# ----------------------------
@auth_bp.route("/", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        password = data["password"]

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        if users.find_one({"email": email}):
            return jsonify({"error": "User already exists"}), 400

        hashed_pw = generate_password_hash(password)
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_pw,
            "isAdmin": False,
            "createdAt": datetime.utcnow()
        }
        result = users.insert_one(new_user)
        user = users.find_one({"_id": result.inserted_id})

        payload = {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "isAdmin": user["isAdmin"],
        }
        return generate_token(user,payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# @desc    Logout user
# @route   POST /api/users/logout
# @access  Public
# ----------------------------
@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    try:
        resp = make_response(jsonify({"message": "Logged out successfully"}))
        resp.set_cookie("jwt", "", httponly=True,
                        samesite="Strict", expires=0)
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
#  Get user profile
# ----------------------------
@auth_bp.route("/profile", methods=["GET"])
def get_user_profile():
    try:
        token = request.cookies.get("jwt")
        if not token:
            return jsonify({"error": "Not authorized, no token"}), 401

        decoded = decode_token(token)
        if not decoded:
            return jsonify({"error": "Not authorized, token failed"}), 401

        user = users.find_one({"_id": ObjectId(decoded["user_id"])})
        if user:
            return jsonify({
                "_id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "isAdmin": user.get("isAdmin", False),
            })

        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# @desc    Update user profile
# @route   PUT /api/users/profile
# @access  Private
# ----------------------------
@auth_bp.route("/profile", methods=["PUT"])
def update_user_profile():
    try:
        token = request.cookies.get("jwt")
        if not token:
            return jsonify({"error": "Not authorized, no token"}), 401

        decoded_user_id = decode_token(token)
        if not decoded_user_id:
            return jsonify({"error": "Not authorized, token failed"}), 401

        # Ensure user exists
        user = users.find_one({"_id": ObjectId(decoded_user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json() or {}
        updated_fields = {}

        if "name" in data and data["name"]:
            updated_fields["name"] = data["name"]
        if "email" in data and data["email"]:
            updated_fields["email"] = data["email"]
        if "password" in data and data["password"]:
            updated_fields["password"] = generate_password_hash(data["password"])

        if updated_fields:
            result = users.update_one({"_id": user["_id"]}, {"$set": updated_fields})
            print("Matched:", result.matched_count, "Modified:", result.modified_count)

        updated_user = users.find_one({"_id": user["_id"]})
        return jsonify({
            "_id": str(updated_user["_id"]),
            "name": updated_user["name"],
            "email": updated_user["email"],
            "isAdmin": updated_user.get("isAdmin", False),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
