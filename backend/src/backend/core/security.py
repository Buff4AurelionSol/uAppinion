from pwdlib import PasswordHash
import jwt
from datetime import datetime, timezone, timedelta
from backend.core.config import settings
from fastapi import HTTPException, status
import secrets
import hashlib

password_hash = PasswordHash.recommended()

def create_hash_password(password: str):
    return password_hash.hash(password)

def verify_hash_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(
        data:dict, 
        expires_delta: timedelta | None = None
) -> str:
    
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else: 
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "access"
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

