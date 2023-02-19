import pytest
from httpx import AsyncClient
from fastapi import status

from admin.auth.auth_utils import verify_password, get_password_hash
from mock import AuthUserDBGenerator
from settings import settings


def _verify_password(password, hashed_password):
    return verify_password(password, hashed_password)


def _update_generator_password(generator: AuthUserDBGenerator):
    password = generator.fields['password']
    hashed_password = get_password_hash(password)
    generator.update(password=hashed_password)
    return generator


@pytest.mark.asyncio
# @pytest.mark.skip(reason='Пока что не готова апишка')
async def test_user_login(client: AsyncClient):
    generator = _update_generator_password(AuthUserDBGenerator())
    await generator.generate_mock_data()

    client.headers.update({'content-type': 'application/x-www-form-urlencoded'})

    response = await client.post(f'{settings.PROXY_PREFIX}/auth/login', data={'username': 'pten4uk', 'password': '12345678'})
    data = response.json()

    assert response.status_code == status.HTTP_200_OK, 'Неверный статус ответа'
    assert 'access_token' in data, 'В ответе нет ключа "access_token"'

