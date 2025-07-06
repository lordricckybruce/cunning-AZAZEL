# python_controller/utils.py
from cryptography.fernet import Fernet
import os

KEY_FILE = "encryption.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    return open(KEY_FILE, "rb").read()

fernet = Fernet(load_key())

def encrypt_message(message: str) -> bytes:
    return fernet.encrypt(message.encode())

def decrypt_message(token: bytes) -> str:
    return fernet.decrypt(token).decode()

