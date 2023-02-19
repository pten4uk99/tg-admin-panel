from fastapi import Depends
from jose import jwt, JWTError

from admin.auth.auth_dao import AuthUserDB
from admin.auth.auth_deps import oauth2_scheme
from admin.auth.auth_models import TokenData
from admin.auth.auth_exceptions import ObjectExist, Unauthorized
from admin.auth.auth_utils import get_password_hash, verify_password
from settings import settings


async def create_auth_user(username: str, password: str):
    """
    Создает пользователя в базе данных.
    Хэширует пароль.
    Выбрасывает исключение если пользователь уже существует.
    """

    user = await AuthUserDB.get_or_none(username=username)
    if user is not None:
        raise ObjectExist('Пользователь существует в базе данных')

    hashed_password = get_password_hash(password)
    await AuthUserDB.create(username=username, password=hashed_password)


async def find_user(username: str):
    return await AuthUserDB.filter(username=username).first()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Unauthorized()
        token_data = TokenData(username=username)
    except JWTError:
        raise Unauthorized()
    user = find_user(username=token_data.username)
    if user is None:
        raise Unauthorized()
    return user


async def check_user_credentials(username: str, password: str):
    user = await find_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
