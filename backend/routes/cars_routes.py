from flask import Blueprint, request, jsonify, make_response
from bson import ObjectId
from backend import mongo 
from datetime import datetime

cars_bp = Blueprint("cars", __name__)

# Mongo collection
cars = mongo.db.cars

##Get all cars
@cars_bp.route("", methods=["GET"])
def get_all_cars():
    try:
        cars=list(mongo.db.cars.find())
        for car in cars:
            car["_id"]= str(car["_id"])
        return jsonify(cars),200
    except Exception as err:
        return jsonify({"error": str(err)}), 400

#Get a car
@cars_bp.route("/<id>",methods=["GET"])
def get_car(id):
    try:
        car=cars.find_one({"_id":ObjectId(id)})
        if not car:
            return jsonify({"Error":"Car not found"})
        car["_id"]=str(car["_id"])
        return jsonify(car), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    

## Search cars with city
@cars_bp.route("/search/<location>",methods=["GET"])
def Search_cars(location):
    try:
        query={"location": {"$regex": location, "$options": "i"}}
        cars=list(mongo.db.cars.find(query))
        for car in cars:
            car["_id"]=str(car["_id"])
        return jsonify({"car":cars}),200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 400
