from typing import Type

import pytest
from httpx import AsyncClient

from settings import settings
from tests.generator import MockGenerator
from tests.mock import CombotUserDBGenerator, CombotChatDBGenerator


@pytest.mark.asyncio
@pytest.mark.parametrize(('generator', 'url_postfix', 'db_objects_quantity',), [
    (CombotUserDBGenerator, 'users', 0),
    (CombotUserDBGenerator, 'users', 1),
    (CombotUserDBGenerator, 'users', 5),
    (CombotChatDBGenerator, 'chats', 0),
    (CombotChatDBGenerator, 'chats', 1),
    (CombotChatDBGenerator, 'chats', 5),
])
async def test_get_users(client: AsyncClient, generator: Type[MockGenerator], url_postfix: str, db_objects_quantity: int):
    await generator().generate_mock_data(db_objects_quantity)

    response = await client.get(f'{settings.PROXY_PREFIX}/combot/{url_postfix}')
    data = response.json()

    assert len(data) == db_objects_quantity, 'Неверное количество объектов'


@pytest.mark.asyncio
@pytest.mark.parametrize(('generator', 'url_postfix', 'db_objects_quantity', 'result_len_data'), [
    (CombotUserDBGenerator, 'users', 0, 0),
    (CombotUserDBGenerator, 'users', 1, 1),
    (CombotChatDBGenerator, 'chats', 0, 0),
    (CombotChatDBGenerator, 'chats', 1, 1),
])
async def test_get_user(client: AsyncClient, generator, url_postfix, db_objects_quantity, result_len_data):
    await generator().update(id=1).generate_mock_data(db_objects_quantity)

    response = await client.get(f'{settings.PROXY_PREFIX}/combot/{url_postfix}/1')
    data = response.json()

    assert len(data) == result_len_data, 'Неверное количество объектов'
