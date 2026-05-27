from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets

from jose import JWTError, jwt

from app.core.config import get_settings


HASH_NAME = "sha256"
ITERATIONS = 210_000
SALT_BYTES = 16


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        hash_name, iterations, salt, expected_hash = hashed_password.split("$", 3)
    except ValueError:
        return False

    password_hash = _hash_password(
        plain_password,
        bytes.fromhex(salt),
        int(iterations),
        hash_name,
    )
    return hmac.compare_digest(password_hash, expected_hash)


def get_password_hash(password: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    password_hash = _hash_password(password, salt, ITERATIONS, HASH_NAME)
    return f"{HASH_NAME}${ITERATIONS}${salt.hex()}${password_hash}"


def _hash_password(password: str, salt: bytes, iterations: int, hash_name: str) -> str:
    return hashlib.pbkdf2_hmac(
        hash_name,
        password.encode("utf-8"),
        salt,
        iterations,
    ).hex()


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> str | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        subject = payload.get("sub")
    except JWTError:
        return None
    return subject if isinstance(subject, str) else None
