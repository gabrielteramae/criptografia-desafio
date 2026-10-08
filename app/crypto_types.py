from sqlalchemy.types import TypeDecorator, String
from cryptography.fernet import InvalidToken
from app.crypto import encrypt, decrypt


class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return encrypt(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        try:
            return decrypt(value)
        except InvalidToken:
            return None
