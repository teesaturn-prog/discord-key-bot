
import os
from flask import Flask, request, jsonify
from database import verify_key

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online"})

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(silent=True) or {}

    key = data.get("key")
    discord_id = data.get("discord_id")

    if not isinstance(key, str) or not isinstance(discord_id, str):
        return jsonify({
            "valid": False,
            "message": "Invalid request"
        }), 400

    if len(key) > 100 or len(discord_id) > 30:
        return jsonify({"valid": False}), 400

    valid = verify_key(key, discord_id)

    return jsonify({
        "valid": valid,
        "message": "Accepted" if valid else "Invalid or expired key"
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
