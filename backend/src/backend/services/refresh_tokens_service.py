from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.refresh_tokens import CreateRefreshTokens
from backend.schemas.auth import TokenResponse
from backend.models.refresh_tokens import RefreshToken
from backend.models.user import User
from backend.services.user_service import get_user
from backend.core.security import hash_token, generate_refresh_token, create_access_token
from sqlalchemy import select, update
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from backend.core.config import settings



async def create_refresh_token(
        db: AsyncSession,
        token: CreateRefreshTokens
) -> RefreshToken:

    new_token_hash = RefreshToken(
        token_hash=token.token_hash,
        user_id=token.user_id,
        expires_at=token.expires_at,
        user_agent=token.user_agent
    )

    db.add(new_token_hash)
    await db.commit()
    await db.refresh(new_token_hash)
    return new_token_hash


async def get_refresh_token(db: AsyncSession, token_hash: str) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    db_token = await db.execute(stmt)
    return db_token.scalars().first()


async def revoke_user_token(db:AsyncSession, token_id: str) -> None:
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.id == token_id)
        .values(revoked=True)
    )
    await db.execute(stmt)
    await db.commit()


async def revoke_all_user_tokens(db:AsyncSession, user_id: str) -> None:
    stmt = update(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False
    ).values(revoked=True)
    await db.execute(stmt)
    await db.commit()

async def renew_refresh_token(db: AsyncSession, plain_refresh_token: str):
    token_hash = hash_token(plain_refresh_token)
    stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    existRefreshToken = await db.scalar(stmt)

    if not existRefreshToken: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    if existRefreshToken.revoked == True: 
        await revoke_all_user_tokens(db, existRefreshToken.user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token comprometido. Inicie sesión nuevamente."
        )

    if existRefreshToken.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado."
        )
    stmt = select(User).where(User.id == existRefreshToken.user_id)
    user = await db.scalar(stmt)

    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )
    existRefreshToken.revoked = True
    new_access_token = create_access_token({"sub": str(user.id)})
    new_plain_refresh_token = generate_refresh_token()
    refresh_token_hashed = hash_token(new_plain_refresh_token)

    new_refresh_token_dto = RefreshToken(
        token_hash=refresh_token_hashed,
        user_id=user.id,
        expires_at= datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(new_refresh_token_dto)
    await db.commit()

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_plain_refresh_token,
        token_type="bearer"
    )