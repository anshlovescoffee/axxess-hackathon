from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import psycopg2
import os
import atexit

app = Flask(__name__)
CORS(app)

inventory = pd.read_csv('sample_data_ext.csv')
inventory.set_index('item', inplace=True)

# Insert data
conn = psycopg2.connect( 
    database="db",
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"]
) 
cursor = conn.cursor()

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

@app.route('/update_item')
def set_inventory_item():
    item = request.args.get('item')
    change = float(request.args.get('change'))

    if not item:
        return jsonify({'message:' 'No item given'})

    if item.lower() not in inventory['item'].unique():
        return f'No item {item.lower()} found in inventory'

    inventory.loc[inventory.index == item, 'quantity'] = inventory['quantity'] + change 

    return jsonify({'message': 'Success'})

def cleanup():
    cursor.close()
    conn.close()
atexit.register(cleanup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
