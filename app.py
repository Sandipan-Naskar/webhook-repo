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
    print("✅ Webhook data received:", data)

    # Extract info from real GitHub payload
    author = data.get("head_commit", {}).get("author", {}).get("name", "unknown")
    to_branch = data.get("ref", "").split("/")[-1]  # e.g. refs/heads/main → main

    payload = {
        "request_id": data.get("after", ""),  # commit hash
        "author": author,
        "action": "PUSH",
        "from_branch": "",  # Not available in push event
        "to_branch": to_branch,
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    }

    events.insert_one(payload)
    print("✅ Event stored:", payload)
    return jsonify({"msg": "Event stored"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    all_events = list(events.find({}, {"_id": 0}))
    print(f" {len(all_events)} event(s) fetched.")
    return jsonify(all_events)

if __name__ == "__main__":
    print(" Flask server starting on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
