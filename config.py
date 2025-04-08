import os
from cryptography.fernet import Fernet

def get_or_create_encryption_key():
    key_path = '.encryption_key'
    if os.path.exists(key_path):
        with open(key_path, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as f:
            f.write(key)
        return key

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///password_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENCRYPTION_KEY = get_or_create_encryption_key().decode()
