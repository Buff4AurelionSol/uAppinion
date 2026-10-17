from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.auth import AuthenticationRequest, TokenResponse
from backend.schemas.refresh_tokens import CreateRefreshTokens
from backend.schemas.user import ResponseUser
from backend.services.user_service import get_user_entity_by_email
from backend.services.refresh_tokens_service import create_refresh_token, get_refresh_token, revoke_user_token
from backend.core.security import verify_hash_password, create_access_token, generate_refresh_token, hash_token, decode_access_token
from backend.core.config import settings
from backend.models.user import User
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from backend.config.db import get_db
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def authenticate_user(db: AsyncSession, authData: AuthenticationRequest) -> User:
    user = await get_user_entity_by_email(db, authData.email)
    if not user or not verify_hash_password(authData.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
    

async def login(
        db: AsyncSession, 
        authData: AuthenticationRequest,
        user_agent: str | None = None
) -> TokenResponse: 
    user = await authenticate_user(db, authData)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    raw_refresh_token = generate_refresh_token()
    token_hash = hash_token(raw_refresh_token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    token_dto = CreateRefreshTokens(
        token_hash=token_hash,
        user_id=str(user.id),
        user_agent=user_agent,
        expires_at=expires_at
    )

    await create_refresh_token(db, token_dto)
    
    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token
    }



async def logout(db: AsyncSession, refresh_token: str):

    token_hash = hash_token(refresh_token)
    existing_refresh_hash = await get_refresh_token(db, token_hash)
    if existing_refresh_hash and not existing_refresh_hash.revoked:
        await revoke_user_token(db, existing_refresh_hash.id)

    return {"detail": "Sesión cerrada exitosamente."}

async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token : str = Depends(oauth2_scheme),
     
) -> ResponseUser: 
    
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    stmt = select(User).where(User.id == user_id)
    user = await db.scalar(stmt)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return ResponseUser.model_validate(user)