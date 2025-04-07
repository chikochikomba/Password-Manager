import bcrypt
from cryptography.fernet import Fernet
import base64
import os

class PasswordManager:
    def __init__(self, key=None):
        if key is None:
            key = base64.urlsafe_b64encode(os.urandom(32))
        self.key = key
        self.cipher_suite = Fernet(self.key)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)

    def encrypt_password(self, plain_password):
        return self.cipher_suite.encrypt(plain_password.encode())

    def decrypt_password(self, encrypted_password):
        return self.cipher_suite.decrypt(encrypted_password).decode()
