from bson import ObjectId
from flask import Blueprint, jsonify, make_response, request
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
            return_document=ReturnDocument.AFTER,  # ✅ this returns updated doc
        )
        print(booking)

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
