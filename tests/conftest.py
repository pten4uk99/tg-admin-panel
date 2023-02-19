import asyncio

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from main import app


def _sync_init():
    """Initial database connection"""

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise.init(
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "telegram.communication_bot.combot_dao",
                "admin.auth.auth_dao"
            ]
        },
        _create_db=True
    ))
    loop.run_until_complete(Tortoise.generate_schemas())


def _sync_out():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Tortoise._drop_databases())


@pytest.fixture(scope="function", autouse=True)
def initialize_tests():
    _sync_init()
    yield
    _sync_out()


@pytest.fixture(scope="function")
def client():
    yield AsyncClient(app=app, base_url="http://test")


