from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.refresh_tokens import CreateRefreshTokens
from backend.models.refresh_tokens import RefreshToken
from sqlalchemy import select, update



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