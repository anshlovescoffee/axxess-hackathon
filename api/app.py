from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from React frontend

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

@app.route("/patients")
def patients():
    return jsonify({"patients": ["John Doe", "Jane Smith", "Alice Johnson"]})

@app.route("/inventory")
def inventory():
    return jsonify({"inventory": ["Wheelchair", "Bandages", "Medications"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask is reachable
