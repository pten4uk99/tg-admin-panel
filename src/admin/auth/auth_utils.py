from datetime import timedelta, datetime

from jose import jwt

from admin.auth.auth_deps import pwd_context
from settings import settings


def verify_password(plain_password: str, hashed_password: str):
    """ Проверяет соответствие оригинального пароля его хэшу """

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """ Хэширует пароль """

    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
