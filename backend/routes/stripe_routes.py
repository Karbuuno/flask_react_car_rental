import os
from flask import Blueprint, request, jsonify
from bson import ObjectId
from backend import mongo 
import stripe


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET_KEY")
CLIENT_URL = os.getenv("CLIENT_URL")


stripe_bp = Blueprint("stripe", __name__)

# Mongo collection
cars = mongo.db.cars
users = mongo.db.users
bookings = mongo.db.bookings

## create checkout session
@stripe_bp.route("/create_checkout_session", methods=["POST"])
def create_checkout_session():
    try:
        data=request.get_json()
        print("image:",data["image"])
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name":data['make'],
                        "images": [data["image"]],},
                        "unit_amount": int(float(data["totalPrice"]) * 100),
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": data["userId"],
                "carId": data["carId"],
                "make": data["make"],
                "image":data["image"],
                "regNumber": data["regNumber"],
                "startDate": data["startDate"],
                "endDate": data["endDate"],
                "isAvailable": False,
                "totalPrice":float(data["totalPrice"]),
                "totalDays": int(data["totalDays"]),
            },
            success_url=f"{CLIENT_URL}/success",
            cancel_url=f"{CLIENT_URL}/cancel",
        )

        return jsonify({"url": session.url})
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    

    # ----------------- Stripe Webhook -----------------
@stripe_bp.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # convert types properly
        booking = {
            "userId": session["metadata"]["user_id"],
            "carId": session["metadata"]["carId"],
            "make": session["metadata"]["make"],
            "image": session["metadata"]["image"],
            "regNumber": session["metadata"]["regNumber"],
            "startDate": session["metadata"]["startDate"], 
            "endDate": session["metadata"]["endDate"],

            "isAvailable": False,  
            "totalPrice": float(session["metadata"]["totalPrice"]),  
            "totalDays": int(session["metadata"]["totalDays"]),      
            "payment_status": session["payment_status"],
            "created_at": int(session["created"]),  
        }

        bookings.insert_one(booking)

        # update car availability in cars collection
        cars.update_one(
            {"_id": ObjectId(session["metadata"]["carId"])},
            {"$set": {"isAvailable": False}}
        )

    return jsonify({"status": "success"}), 200
