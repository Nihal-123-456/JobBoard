import string
import secrets

def generate_django_secret_key():
    chars = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(secrets.choice(chars) for _ in range(50))
    return key

print(generate_django_secret_key())