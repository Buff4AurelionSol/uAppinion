from fastapi import APIRouter, Depends, status, Response, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config.db import get_db
from backend.schemas.auth import AuthenticationRequest, TokenResponse
from backend.schemas.user import ResponseUser
from backend.services.auth import login, logout, get_current_user
from backend.services.refresh_tokens_service import renew_refresh_token
from backend.core.config import settings

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_user(
    authData: AuthenticationRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    auth_result = await login(db, authData)
    #Dias a Minutos a Horas y luego segundos
    expires_refresh_token_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    
    response.set_cookie(
        key="refresh_token",
        value=auth_result["refresh_token"],
        httponly=True,
        samesite="lax",
        #El valor de secure debe estar el True en producción.
        secure=False,
        max_age=expires_refresh_token_seconds,
        path="/"
    )
    return TokenResponse(
        access_token=auth_result["access_token"],
        token_type="bearer"
    )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    if refresh_token:
        await logout(db, refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {"detail": "Sesión cerrada exitosamente"}

@router.post("/refresh", response_model=TokenResponse)
async def get_a_renew_refresh_token(
    response: Response,
    plain_refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db), 
    
):
     if not plain_refresh_token:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="No se encontró el token actualizado"
         )
     
     auth_result = await renew_refresh_token(db, plain_refresh_token)
     expires_refresh_token_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
     response.set_cookie(
        key="refresh_token",
        value=auth_result["refresh_token"],
        httponly=True,
        samesite="lax",
        #El valor de secure debe estar el True en producción.
        secure=False,
        max_age=expires_refresh_token_seconds,
        path="/"
    )

     return TokenResponse(
         access_token=auth_result["access_token"],
         token_type="bearer"
     )


@router.get("/me", response_model=ResponseUser)
async def read_current_user(
    current_user: ResponseUser = Depends(get_current_user)
):
    return current_user
