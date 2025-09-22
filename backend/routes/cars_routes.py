import base64

import cloudinary
import cloudinary.uploader
from bson import ObjectId
from flask import Blueprint, jsonify, request
from pymongo import ReturnDocument

from backend import mongo

cars_bp = Blueprint("cars", __name__)

# Mongo collection
cars_cl = mongo.db.cars
bookings_cl = mongo.db.bookings


##Get all cars
@cars_bp.route("", methods=["GET"])
def get_all_cars():
    try:
        cars = list(cars_cl.find())
        for car in cars:
            car["_id"] = str(car["_id"])
        return jsonify(cars), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400


# Get a car
@cars_bp.route("/<id>", methods=["GET"])
def get_car(id):
    try:
        car = cars_cl.find_one({"_id": ObjectId(id)})
        if not car:
            return jsonify({"Error": "Car not found"})
        car["_id"] = str(car["_id"])
        return jsonify(car), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400


## Search cars with city
@cars_bp.route("/search/<location>", methods=["GET"])
def Search_cars(location):
    try:
        query = {"location": {"$regex": location, "$options": "i"}}
        cars = list(cars_cl.find(query))
        for car in cars:
            car["_id"] = str(car["_id"])
        return jsonify({"car": cars}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 400


#  Add Car
@cars_bp.route("/add_car", methods=["POST"])
def add_car():
    try:
        data = request.form.to_dict()
        image_url = None

        if "price" in data:
            data["price"] = float(data["price"])
        if "seats" in data:
            data["seats"] = int(data["seats"])

        if "file" in request.files:
            file = request.files["file"]
            result = cloudinary.uploader.upload(file, resource_type="image")
            image_url = result.get("secure_url")

        data["image"] = image_url
        data["isAvailable"] = True

        car_id = cars_cl.insert_one(data).inserted_id
        data["_id"] = str(car_id)
        return jsonify(data), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@cars_bp.route("/available/<id>", methods=["PATCH"])
def available_car(id):
    try:
        data = request.get_json()
        is_available = data.get("isAvailable", True)

        # Update booking
        booking = bookings_cl.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"isAvailable": is_available}},
            return_document=ReturnDocument.AFTER,
        )

        if not booking:
            return jsonify({"error": "Booking Not Found"}), 400

        # Update car linked to booking
        car = cars_cl.find_one_and_update(
            {"_id": ObjectId(booking["carId"])},
            {"$set": {"isAvailable": is_available}},
            return_document=ReturnDocument.AFTER,
        )

        if not car:
            return jsonify({"error": "Car Not Found"}), 400

        return jsonify({"available": car}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Car not found"}), 404


#  Update Car
@cars_bp.route("/update/<car_id>", methods=["PUT"])
def update_car(car_id):
    try:
        if request.form:
            update_data = request.form.to_dict()
        else:
            update_data = request.get_json() or {}

        # 🧹 Normalize keys (important!)
        update_data = {k.strip(): v for k, v in update_data.items()}

        # Convert numeric fields
        if "price" in update_data:
            update_data["price"] = float(update_data["price"])
        if "seats" in update_data:
            update_data["seats"] = int(update_data["seats"])
        if "doors" in update_data:
            update_data["doors"] = int(update_data["doors"])

        # Handle image upload
        if "file" in request.files:
            file = request.files["file"]
            result = cloudinary.uploader.upload(file, resource_type="image")
            update_data["image"] = result.get("secure_url")

        updated_car = cars_cl.find_one_and_update(
            {"_id": ObjectId(car_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )

        if updated_car:
            updated_car["_id"] = str(updated_car["_id"])
            return jsonify(updated_car), 200
        else:
            return jsonify({"error": "Car not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


#  Delete Car
@cars_bp.route("/delete/<car_id>", methods=["DELETE"])
def delete_car(car_id):
    try:
        result = cars_cl.delete_one({"_id": ObjectId(car_id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Car deleted successfully"}), 200
        else:
            return jsonify({"error": "Car not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
