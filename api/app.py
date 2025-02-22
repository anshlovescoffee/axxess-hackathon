from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from React frontend

# Sample data
inventory = pd.DataFrame([
    {
        "item": "Wheelchair",
        "quantity": 10,
        "restock_threshold": 5
    },
    {
        'item': 'Bandages',
        'quantity': 100,
        'restock_threshold': 50
    },
    {
        'item': 'Medications',
        'quantity': 50,
        'restock_threshold': 25
    }
])

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

# TODO: implement
@app.route('/patient')
def find_patient():
    return jsonify({"message": "Patient not found"})

@app.route("/inventory")
def inventory():
    return jsonify(inventory.to_dict())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask is reachable
