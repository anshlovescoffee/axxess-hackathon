import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Ensure the inventory generator script is used
from gen_inventory import inventory

app = Flask(__name__)
CORS(app)

# Load inventory (ensures sample_data.csv is used)
csv_file = "sample_data.csv"
if not os.path.exists(csv_file):
    inventory.to_csv(csv_file, index=False)

inventory = pd.read_csv(csv_file)
inventory.set_index("item", inplace=True)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory.to_dict(orient='index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
