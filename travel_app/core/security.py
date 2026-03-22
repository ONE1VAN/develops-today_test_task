import bcrypt

MAX_BCRYPT_LENGTH = 72

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:MAX_BCRYPT_LENGTH]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode()

def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode("utf-8")[:MAX_BCRYPT_LENGTH]
    return bcrypt.checkpw(password_bytes, password_hash.encode())
