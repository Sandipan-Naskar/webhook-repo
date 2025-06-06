print("Starting app...")

from flask import Flask, request, jsonify, render_template
from models.db import events
from datetime import datetime
from flask_cors import CORS

print("Flask imports done...")

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(" Webhook data received:", data)

    action_type = data.get("action_type")
    payload = {
        "request_id": data.get("request_id"),
        "author": data.get("author"),
        "action": action_type,
        "from_branch": data.get("from_branch"),
        "to_branch": data.get("to_branch"),
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    }
    events.insert_one(payload)
    print(" Event stored:", payload)
    return jsonify({"msg": "Event stored"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    all_events = list(events.find({}, {"_id": 0}))
    print(f" {len(all_events)} event(s) fetched.")
    return jsonify(all_events)

if __name__ == "__main__":
    print(" Flask server starting on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
