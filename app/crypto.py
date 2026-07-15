from cryptography.fernet import Fernet
import os

_key = os.getenv("ENCRYPTION_KEY")

if not _key:
    _key = Fernet.generate_key().decode()
    print(f"[crypto] ENCRYPTION_KEY nao definida, usando chave temporaria: {_key}")

_fernet = Fernet(_key.encode())


def encrypt(value: str) -> str:
    if value is None:
        return None
    return _fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    if value is None:
        return None
    return _fernet.decrypt(value.encode()).decode()
