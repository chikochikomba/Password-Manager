 ## 🔒 Secure Password Manager
 
A secure, Flask-based web application for storing, generating, and managing passwords with strong encryption to protect user credentials.

## Overview
The Secure Password Manager is a user-friendly and robust web application designed to help individuals securely store and manage their passwords. Built using the Flask framework, this application integrates encryption mechanisms to ensure that all user credentials are stored safely.

## Key Features
**Master Password Authentication:** Users authenticate via a master password to securely access stored credentials.

**Password Storage:** Safely store usernames and passwords for various services, all encrypted.

**Password Generation:** Generate strong, customizable passwords with adjustable length and options to include symbols, numbers, or special characters.

**User Management:** Add, view, update, and delete stored credentials with ease.

**Eryption:** Passwords are encrypted using the cryptography library, ensuring data security at rest.

## Screenshots






## Setup Instructions

1. Clone the Repository

       git clone https://github.com/yourusername/secure-password-manager.git
       cd secure-password-manager

3. Create and Activate Virtual Environment

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies

       pip install -r requirements.txt
   
5. Initialize the Database

       python init_db.py

## Usage
1. Start the Development Server
 
       python app.py

   
3. Access the Application
   
       Navigate to  http://127.0.0.1:5000 in your browser.

5. First-Time Setup
   
       Register a new account.

       Log in with your credentials.

       Start adding and managing your passwords securely.

## 🔧 Configuration

Set up optional environment variables for enhanced customization:

    export SECRET_KEY='your-very-secret-key'
    export DATABASE_URL='sqlite:///production.db'
    export ENCRYPTION_KEY='your-encryption-key'

## 📂 Project Structure

    secure-password-manager/
    ├── LICENSE
    ├── gitignore
    ├── app.py                # Main application entry point
    ├── config.py             # Configuration settings
    ├── models.py             # Database models
    ├── password_manager.py   # Encryption and decryption logic
    ├── utilities.py          # Password generation utilities
    ├── requirements.txt      # Project dependencies
    ├── init_db.py            # Database initialization script
    ├── static/               # Static files (CSS, JavaScript)
    └── templates/            # HTML templates for views
       ├── login.html
       ├── register.html
       ├── dashboard.html
       └── add_password.html
       
## 🛡️ Security Features

Fernet Encryption: Implements AES-128-CBC with HMAC-SHA256 for secure password storage.

PBKDF2 Password Hashing: Uses salt to securely hash user passwords.

Session Management: Secure handling of user sessions.

CSRF Protection: Enabled via Flask-WTF to prevent cross-site request forgery attacks.

Password Complexity Enforcement: Ensures the creation of strong passwords through customizable rules.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.
