from bson import ObjectId, errors
from flask import Blueprint, jsonify

from backend import mongo

bookings_bp = Blueprint("bookings", __name__)

# Mongo collection
bookings_cl = mongo.db.bookings


# ✅ GET all bookings
@bookings_bp.route("/", methods=["GET"])
def get_all_bookings():
    try:
        bookings = list(bookings_cl.find())
        for booking in bookings:
            booking["_id"] = str(booking["_id"])
        return jsonify(bookings)
    except Exception as err:
        return jsonify({"error": str(err)}), 400


# ✅ GET single booking by id
@bookings_bp.route("/<id>", methods=["GET"])
def get_single_booking(id):
    try:
        booking = bookings_cl.find_one({"_id": ObjectId(id)})
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking["_id"] = str(booking["_id"])
        return jsonify(booking)

    except errors.InvalidId:
        return jsonify({"error": "Invalid booking id"}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    #  Delete Booking


@bookings_bp.route("/delete_booking/<id>", methods=["DELETE"])
def delete_car(id):
    try:
        result = bookings_cl.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Booking deleted successfully"}), 200
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
