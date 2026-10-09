from fastapi import APIRouter, Depends, Query
from backend.services.user_service import get_user, create_user, get_all_users
from backend.config.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user import CreateUser


router = APIRouter()

@router.post("/register")
async def create_new_user(newUser: CreateUser, db: AsyncSession = Depends(get_db)):
    resultUser = await create_user(newUser, db)
    return resultUser

    
@router.get("/{uuid}")
async def get_user_by_id( uuid: str, db: AsyncSession = Depends(get_db)):
    return await get_user(uuid, db)

@router.get("")
async def get_all(db:AsyncSession = Depends(get_db)):
    return await get_all_users(db)
