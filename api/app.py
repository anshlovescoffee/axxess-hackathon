<<<<<<< HEAD
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
=======
from flask import Flask, jsonify
from flask_cors import CORS
>>>>>>> b01fddcaa04e4c074ace2974879df4886b764cb0

app = Flask(__name__)
CORS(app)  # Allows requests from React frontend

<<<<<<< HEAD
# Sample data
inventory = pd.DataFrame({
    "item": ["wheelchair", "bandages", "medications"],
    "quantity": [10, 100, 50],
    "restock_threshold": [5, 50, 25]
})
inventory.set_index(inventory['item'])

print(inventory)
exit()

=======
>>>>>>> b01fddcaa04e4c074ace2974879df4886b764cb0
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

<<<<<<< HEAD
# TODO: finish this shit
@app.route('/patient')
def find_patient():
    result = None

    # some db shit here 

    return jsonify({"message": "Patient not found"})

# @app.route("/inventory")
# def get_inventory():
#     return jsonify(inventory.to_dict(orient='list'))

@app.route('/inventory')
def get_inventory_item():
    search_term = request.args.get('search_term').lower()
    result = inventory.loc[inventory['item'] == search_term]

    return jsonify(result.to_dict(orient='list'))

@app.route('/fill_inventory', methods=['POST'])
def fill_inventory(): 
    inbound = request.get_json()
    inventory = pd.DataFrame(inbound['items'])

    return jsonify({"message": "Inventory updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
=======
@app.route("/patients")
def patients():
    return jsonify({"patients": ["John Doe", "Jane Smith", "Alice Johnson"]})

@app.route("/inventory")
def inventory():
    return jsonify({"inventory": ["Wheelchair", "Bandages", "Medications"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask is reachable
>>>>>>> b01fddcaa04e4c074ace2974879df4886b764cb0
