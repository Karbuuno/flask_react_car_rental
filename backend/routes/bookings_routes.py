from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from backend import mongo 


bookings_bp = Blueprint("bookings", __name__)

# Mongo collection
bookings_cl = mongo.db.bookings

 # GET all bookings
@bookings_bp.route("/",methods=["GET"])
def get_all_bookings():
    try:
        bookings=list(bookings_cl.find())
        for booking in bookings:
            booking["_id"]=str(booking["_id"])
        return jsonify(bookings)
    except Exception as err:
        return jsonify({"Error":str(err)}),400
    
    #GET single car
@bookings_bp.route("/<id>")
def get_single_bookings(id):
    booking=bookings_cl.find_one({"_id":ObjectId(id)})
    if not booking:
        return jsonify({"Error":"Booking not found"})
    booking["_id"]=str(booking["_id"])
    return jsonify(booking)