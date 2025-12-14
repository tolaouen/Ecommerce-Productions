from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
import bcrypt
from app.core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Convert to Unix timestamp (seconds since epoch)
    expire_ts = int(expire.timestamp())
    to_encode.update({"exp": expire_ts})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_token_payload(token: str):
    try: 
        return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
    except JWTError:
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Handles bcrypt's 72-byte limit by encoding the password properly.
    """
    try:
        # Ensure password is encoded to bytes (bcrypt works with bytes)
        password_bytes = plain_password.encode('utf-8')
        # If password is longer than 72 bytes, bcrypt will truncate it
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        # Ensure hashed_password is also bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password)
    except (ValueError, Exception):
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    Handles bcrypt's 72-byte limit by encoding the password properly.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for database storage
    return hashed.decode('utf-8')