from qrcode import QRCode
from Crypto.Cipher import AES
import base64

# Encryption key (must be 16, 24, or 32 bytes long)
key = b'RY/5+Ks4taJLTNgik7YS9ZkWjsmLb/8C'

# Encrypt data
def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# Generate QR code
def generate_qr_code(med_id, quantity):
    data = f"{med_id},{quantity}"
    encrypted_data = encrypt_data(data)
    qr = QRCode(version=1, box_size=10, border=5)
    qr.add_data(encrypted_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"med_{med_id}_qr.png")

# Example usage
generate_qr_code(med_id=1, quantity=5)
