# python_controller/utils/encryption.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

KEY = b"ThisIsASecretKey"  # Must be 16/24/32 bytes

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt(data):
    data = pad(data.encode())
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(data)).decode()

def decrypt(encrypted_data):
    raw = base64.b64decode(encrypted_data)
    iv = raw[:16]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return cipher.decrypt(raw[16:]).rstrip(b"\0").decode()
