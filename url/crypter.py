import bcrypt
from django.conf import settings


class Crypter:
    salt = settings.BCRYPT_SALT.encode('utf-8')

    def __init__(self, text: str):
        self.text = text.encode('utf-8')

    def encrypt(self) -> str:
        return bcrypt.hashpw(self.text, self.salt).decode('utf-8')

    def equals(self, password: str) -> bool:
        return bcrypt.checkpw(self.text, password.encode('utf-8'))
