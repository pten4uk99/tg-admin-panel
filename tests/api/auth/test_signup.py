import json

import pytest
from httpx import AsyncClient
from fastapi import status

from admin.auth.auth_dao import AuthUserDB
from admin.auth.auth_utils import verify_password
from mock import AuthUserDBGenerator
from settings import settings


@pytest.mark.asyncio
async def test_user_success_signup(client: AsyncClient):
    generator = AuthUserDBGenerator()
    data = await client.post(f'{settings.PROXY_PREFIX}/auth/signup', json=generator.fields)
    users = await AuthUserDB.all()

    assert len(users) == 1, 'Неверное количество пользователей в БД'
    assert data.status_code == status.HTTP_201_CREATED, 'Неверный статус ответа от сервера'


@pytest.mark.asyncio
async def test_password_was_hashed(client: AsyncClient):
    generator = AuthUserDBGenerator()
    await client.post(f'{settings.PROXY_PREFIX}/auth/signup', json=generator.fields)
    user = await AuthUserDB.first()

    assert verify_password(generator.fields['password'], user.password), 'Пароль неверно захеширован'


@pytest.mark.asyncio
async def test_user_exists_exception(client: AsyncClient):
    generator = AuthUserDBGenerator()
    await generator.generate_mock_data()
    response = await client.post(f'{settings.PROXY_PREFIX}/auth/signup', json=generator.fields)
    data = response.json()

    assert 'detail' in data, 'Нет ключа detail в ответе'
