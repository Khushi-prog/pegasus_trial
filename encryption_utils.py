from cryptography.fernet import Fernet

# Generate your key securely once, then reuse
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

def encrypt(message):
    return fernet.encrypt(message.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()