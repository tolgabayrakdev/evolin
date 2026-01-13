from datetime import datetime, timedelta
from typing import Optional

import jwt
from pwdlib import PasswordHash

from ..config.settings import settings

password_hasher = PasswordHash.recommended()


def generate_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        **data,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def generate_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    payload = {
        **data,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        
        # Check token type
        if payload.get("type") != token_type:
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)
