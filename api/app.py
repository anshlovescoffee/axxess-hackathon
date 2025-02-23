from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

inventory = pd.read_csv('sample_data_ext.csv')
inventory.set_index('item', inplace=True)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})
  
# TODO: finish this shit
@app.route('/patient')
def find_patient():
    result = None

    # some db searching shit here

    return jsonify({"message": "Patient not found"})

@app.route('/inventory')
def get_inventory():
    return jsonify(inventory.to_dict(orient='index'))

@app.route('/inventory_search')
def get_inventory_item():
    search_term = request.args.get('search_term')

    if not search_term:
        return jsonify({'message': 'No search term given'})

    result = inventory.loc[inventory.index == search_term]
    return jsonify(result.to_dict(orient='index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)