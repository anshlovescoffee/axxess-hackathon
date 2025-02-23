from flask import Flask, request, jsonify
from Cryptodome.Cipher import AES
import base64
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/scan": {"origins": "*"}})

# Encryption key
key = b'RY/5+Ks4taJLTNgik7YS9ZkWjsmLb/8C'

# PostgreSQL connection config
db_config = {
    'host': 'db',
    'port': '5432',
    'database': 'db',
    'user': 'user',
    'password': 'pass'
}

def decrypt_data(encrypted_data):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
    except Exception as e:
        return str(e)

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    try:
        data = request.json
        encrypted_data = data['qr_data']
        decrypted_data = decrypt_data(encrypted_data)
        med_id, quantity = decrypted_data.split(',')

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # PostgreSQL syntax is slightly different
        cursor.execute(
            "UPDATE inventory SET total_quantity = total_quantity - %s WHERE med_id = %s RETURNING med_id",
            (int(quantity), int(med_id))
        )

        # Check if any row was updated
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({"status": "error", "message": "Medicine ID not found"})

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "med_id": med_id, "quantity": quantity})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)