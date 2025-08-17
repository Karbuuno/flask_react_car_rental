from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
import bcrypt
import datetime
from server import mongo

auth_bp = Blueprint("auth", __name__)
users = mongo.db.users


# ---------- Register ----------
@auth_bp.route("/", methods=["POST"])
def register():
    try:
        data = request.json
        if not data or "name" not in data or "email" not in data or "password" not in data:
            return jsonify({"message": "Missing required fields"}), 400

        if users.find_one({"email": data["email"]}):
            return jsonify({"message": "User already exists"}), 400

        hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        users.insert_one({
            "name": data["name"],
            "email": data["email"],
            "password": hashed_pw,
            "createdAt": datetime.datetime.utcnow()
        })
        return jsonify({"message": "User registered successfully"}), 201



    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Login ----------
@auth_bp.route("/auth", methods=["POST"])
def login():
    try:
        data = request.json
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Missing email or password"}), 400

        user = users.find_one({"email": data["email"]})
        if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        token = create_access_token(identity=str(user["_id"]))
        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Profile (Protected) ----------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        user = users.find_one({"_id": ObjectId(current_user)}, {"password": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": str(user["_id"]),
            "email": user["email"],
            "createdAt": user["createdAt"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
