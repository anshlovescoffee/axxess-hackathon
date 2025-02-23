from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Allows requests from React frontend

# Sample data
inventory = pd.DataFrame({
    "item": ["wheelchair", "bandages", "medications"],
    "quantity": [10, 100, 50],
    "restock_threshold": [5, 50, 25]
})
inventory.set_index(inventory['item'])

print(inventory)
exit()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

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
