from flask import request
import jwt, os

def generate_token(user, data):
    from flask import make_response, jsonify
    from datetime import datetime, timedelta

    payload = {
        "user_id": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")

    resp = make_response(jsonify(data))
    resp.set_cookie(
        "jwt",
        token,
        httponly=True,
        secure=os.getenv("FLASK_ENV") != "development",
        samesite="Strict",
        max_age=30*24*60*60
    )
    return resp


def decode_token(token):
    token = request.cookies.get("jwt")
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
