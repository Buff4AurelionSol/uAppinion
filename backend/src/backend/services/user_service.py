
from backend.schemas.user import CreateUser, ResponseUser
from backend.models.user import User
from backend.core.security import create_hash_password
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from pydantic import EmailStr
import asyncio


async def create_user(userData: CreateUser, db: AsyncSession):
    stmt = select(User.id).where(
        or_(User.id == userData.id, 
            User.email == userData.email
            )
        )
    existingUser = await db.scalar(stmt) 

    if existingUser: 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o el correo electrónico ya se encuentra registrado"
        )
    
    hash_password = await asyncio.to_thread(create_hash_password, userData.password)
    newUser = User(
        id=userData.id,
        name=userData.name,
        lastname=userData.lastname,
        email=userData.email,
        password=hash_password
    )
    db.add(newUser)
    await db.commit()
    await db.refresh(newUser)
    return ResponseUser.model_validate(newUser)

async def get_user(uuid: str, db:AsyncSession) -> ResponseUser:
    stmt = select(User).where(User.id == uuid)
    user = await db.scalar(stmt)
    

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el usuario"
        )

    return ResponseUser.model_validate(user)

async def get_user_by_email(db: AsyncSession, email: EmailStr) -> ResponseUser:
    stmt = select(User).where(User.email == email)
    user = await db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un usuario registrado con el correo proporcionado"
        )
    return ResponseUser.model_validate(user)


async def get_user_entity_by_email(db: AsyncSession, email: EmailStr) -> User | None:
    stmt = select(User).where(User.email == email)
    return await db.scalar(stmt)

    
async def get_all_users(db:AsyncSession) -> list[ResponseUser]:
    stmt = select(
        User.id, 
        User.email, 
        User.name, 
        User.lastname,
        User.is_active
    )
    result = await db.execute(stmt)
    users = result.mappings().all()
    return users
    