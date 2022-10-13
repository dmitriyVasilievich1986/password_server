from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from django.conf import settings
from os import environ


class Key:
    def __init__(self, password=None):
        self.key = self._get_key(password)
        self.fernet = Fernet(self.key)

    def _get_key(self, password):
        if password is None:
            return environ["SECRET_KEY"]
        password = password[:32] + settings.SALT[len(password) :]
        self.password = self._get_value(password)
        return urlsafe_b64encode(self.password)

    def _get_value(self, value):
        return value if isinstance(value, bytes) else str(value).encode("utf8")

    def encrypt(self, value):
        value = self._get_value(value)
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        value = self._get_value(value)
        return self.fernet.decrypt(value)
