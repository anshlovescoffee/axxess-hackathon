import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import psycopg2
import os
import atexit
# from Cryptodome.Cipher import AES
import base64
from populate_db import populate_db

app = Flask(__name__)
CORS(app)

key = b'RY/5+Ks4taJLTNgik7YS9ZkWjsmLb/8C'

inventory = pd.read_csv('sample_data_ext.csv')
inventory.set_index('item', inplace=True)

# DB Stuff
prescriptions = pd.read_csv('prescriptions.csv')
visits = pd.read_csv('visits.csv')
patients = pd.read_csv('patients.csv')

# Insert data
conn = psycopg2.connect( 
    database="db",
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"]
) 
cursor = conn.cursor()
populate_db(conn)
conn.commit()
cursor.close()
conn.close()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Hospice Management API"})

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

def decrypt_data(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    data = request.json
    encrypted_data = data['qr_data']
    decrypted_data = decrypt_data(encrypted_data)
    med_id, quantity = decrypted_data.split(',')

    conn = psycopg2.connect(
        database="db",
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE Inventory SET Total_Quantity = Total_Quantity - %s WHERE Med_ID = %s", (int(quantity), int(med_id)))
    conn.commit()
    cursor.close()

    return jsonify({"status": "success", "med_id": med_id, "quantity": quantity})

@app.route('/patients', methods=['GET'])
def get_all_patients():
    conn = psycopg2.connect(
        database="db",
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )
    cursor = conn.cursor()

    try:
        # Fetch all patients from the database
        cursor.execute("SELECT * FROM Patients;")
        patients = cursor.fetchall()

        # Convert results to a list of dictionaries
        patients_list = []
        column_names = [desc[0] for desc in cursor.description]  # Get column names
        for patient in patients:
            patients_list.append(dict(zip(column_names, patient)))

        return jsonify({
            "success": True,
            "patients": patients_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# @app.route('/patients', methods=['GET'])
# def get_all_patients():
#     pid = request.args.get('pid')
#     conn = psycopg2.connect(
#         database="db",
#         user=os.environ['POSTGRES_USER'],
#         password=os.environ['POSTGRES_PASSWORD'],
#         host=os.environ["POSTGRES_HOST"],
#         port=os.environ["POSTGRES_PORT"]
#     )
#     cursor = conn.cursor()
#
#     if not pid:
#         try:
#             # Fetch all patients from the database
#             cursor.execute("SELECT * FROM Patients;")
#             patients = cursor.fetchall()
#
#             # Convert results to a list of dictionaries
#             patients_list = []
#             column_names = [desc[0] for desc in cursor.description]  # Get column names
#             for patient in patients:
#                 patients_list.append(dict(zip(column_names, patient)))
#
#             return jsonify({
#                 "success": True,
#                 "patients": patients_list
#             }), 200
#
#         except Exception as e:
#             return jsonify({
#                 "success": False,
#                 "error": str(e)
#             }), 500
#
#         finally:
#             cursor.close()
#             conn.close()
#
#         # Specific id
#         cursor.execute('SELECT * FROM Patients WHERE PID = %s;', (pid,))
#         patient = cursor.fetchone()
#
#         if not patient:
#             return jsonify({
#             "success": False,
#             "error": "Patient not found"
#             }), 404
#
#         return jsonify({
#             "success": True,
#             "patient": dict(zip(column_names, patient))
#         }), 200
#
def cleanup():
    cursor.close()
    conn.close()
atexit.register(cleanup)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory.to_dict(orient='index'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
