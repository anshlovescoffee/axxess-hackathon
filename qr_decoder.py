from flask import Flask, request, jsonify
from Cryptodome.Cipher import AES
import base64
import mysql.connector

app = Flask(__name__)
from flask_cors import CORS

CORS(app)  # Enable CORS

# Encryption key (must match the one used for encryption)
key = b'RY/5+Ks4taJLTNgik7YS9ZkWjsmLb/8C'

# Decrypt data
def decrypt_data(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
# API endpoint
@app.route('/scan', methods=['POST'])
def scan_qr_code():
    data = request.json
    encrypted_data = data['qr_data']
    decrypted_data = decrypt_data(encrypted_data)
    med_id, quantity = decrypted_data.split(',')

    

    cursor = db.cursor()
    cursor.execute("UPDATE Inventory SET Total_Quantity = Total_Quantity - %s WHERE Med_ID = %s", (int(quantity), int(med_id)))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"status": "success", "med_id": med_id, "quantity": quantity})

if __name__ == '__main__':
    app.run(debug=True)