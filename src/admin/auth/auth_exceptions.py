from fastapi import HTTPException
from starlette import status


class Unauthorized(HTTPException):
    def __init__(self, detail: str = ''):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ObjectExist(Exception):
    """ Объект уже существует в БД """


