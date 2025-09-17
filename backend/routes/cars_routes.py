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


# ✅ Update a car
@cars_bp.route("/<id>", methods=["PUT"])
def update_car(id):
    try:
        # Use request.form for text fields (multipart/form-data)
        updated_fields = {
            "name": request.form.get("name"),
            "regNumber": request.form.get("regNumber"),
            "seats": request.form.get("seats"),
            "doors": request.form.get("doors"),
            "carType": request.form.get("carType"),
            "gear": request.form.get("gear"),
            "description": request.form.get("description"),
            "location": request.form.get("location"),
            "fuel": request.form.get("fuel"),
            "model": request.form.get("model"),
            "price": request.form.get("price"),
        }

        # ✅ If a file was uploaded
        if "file" in request.files:
            file = request.files["file"]

            # Upload directly to Cloudinary (no need for base64)
            result = cloudinary.uploader.upload(
                file,
                resource_type="image",
                transformation=[{"width": 500, "height": 500, "crop": "limit"}],
            )
            updated_fields["image"] = result.get("secure_url")

        # ✅ Update car in MongoDB
        car = cars_cl.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {k: v for k, v in updated_fields.items() if v is not None}},
            return_document=ReturnDocument.AFTER,
        )

        if not car:
            return jsonify({"error": "Car not found"}), 404

        car["_id"] = str(car["_id"])
        return jsonify(car), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to update car"}), 400
