from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from backend import mongo 
from datetime import datetime

cars_bp = Blueprint("cars", __name__)

# Mongo collection
cars = mongo.db.users

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    cars=list(mongo.db.cars.find())
    for car in cars:
        car["_id"]= str(car["_id"])
        return jsonify(cars),200