from datetime import timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from admin.auth.auth_deps import router
from admin.auth.auth_exceptions import ObjectExist, Unauthorized
from admin.auth.auth_models import AuthUserDBPydantic, Token
from admin.auth.auth_services import create_auth_user, check_user_credentials
from admin.auth.auth_utils import create_access_token
from src.settings import settings


@router.post('/signup', response_model=None, status_code=status.HTTP_201_CREATED)
async def signup(body: AuthUserDBPydantic):
    try:
        await create_auth_user(username=body.username, password=body.password)
    except ObjectExist as e:
        raise HTTPException(detail=str(e), status_code=400)


# пока что не рабочая
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await check_user_credentials(form_data.username, form_data.password)
    if not user:
        raise Unauthorized('Неверный логин или пароль')
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')
