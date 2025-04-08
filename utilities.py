import secrets
import string

def generate_password(length=12, use_digits=True, use_symbols=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        # Ensure password meets complexity requirements
        if (not use_digits or any(c.isdigit() for c in password)) and \
           (not use_symbols or any(c in string.punctuation for c in password)):
            return password