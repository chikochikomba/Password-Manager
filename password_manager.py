from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class PasswordManager:
    def __init__(self, key=None):
        if isinstance(key, str):
            key = key.encode()
        self.cipher_suite = Fernet(key)

    def encrypt_password(self, password):
        if isinstance(password, str):
            password = password.encode()
        return self.cipher_suite.encrypt(password)

    def decrypt_password(self, encrypted_password):
        try:
            return self.cipher_suite.decrypt(encrypted_password).decode()
        except:
            return "*****"  # Return placeholder for invalid tokens
