from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.db import get_db
from backend.schemas.auth import AuthenticationRequest, TokenResponse
from backend.schemas.refresh_tokens import LogoutRequest
from backend.schemas.user import ResponseUser
from backend.services.auth import login, logout, get_current_user
from backend.services.refresh_tokens_service import renew_refresh_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_user(
    authData: AuthenticationRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    return await login(db, authData, response)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    data: LogoutRequest,
    db: AsyncSession = Depends(get_db)
):
    return await logout(db, data.refresh_token)

@router.post("")
async def get_a_renew_refresh_token(
    plan_refresh_token: str,
    response: Response,
    db: AsyncSession = Depends(get_db), 
    
):
    return await renew_refresh_token(db, plan_refresh_token, response)

@router.get("/me", response_model=ResponseUser)
async def read_current_user(
    current_user: ResponseUser = Depends(get_current_user)
):
    return current_user
