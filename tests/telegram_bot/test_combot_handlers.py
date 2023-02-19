from unittest.mock import AsyncMock
import pytest
from aiogram import types

from mock import CombotUserDBGenerator, CombotChatDBGenerator
from telegram.communication_bot.combot_dao import CombotChatDB, CombotUserDB, CombotMessageDB
from telegram.communication_bot.combot_deps import broadcast
from telegram.communication_bot.combot_handlers import _handle_start_command, _handle_private_message


def user_to_python():
    return {
        'id': 1913977763,
        'is_bot': False,
        'first_name': 'Nikita',
        'last_name': 'Pavlenko',
        'username': 'pten4uk',
        'language_code': 'ru'
    }


def chat_to_python():
    return {
        'id': 1913977763,
        'first_name': 'Nikita',
        'last_name': 'Pavlenko',
        'username': 'pten4uk',
        'type': 'private'
    }


@pytest.mark.asyncio
async def test_start_command_handler():
    user = AsyncMock(**user_to_python())
    user.to_python = user_to_python

    chat = AsyncMock(**chat_to_python())
    chat.to_python = chat_to_python

    message = AsyncMock(**{
        'message_id': 1,
        'from_user': user,
        'chat': chat
    })

    await _handle_start_command(message)

    chats_db = await CombotChatDB.all()
    users_db = await CombotUserDB.all()

    message.answer.assert_called_with(f'Здравствуйте {message.from_user.username}! Вы успешно зарегистрированы.')
    assert len(chats_db) == 1, 'Неверное количество чатов создано в БД'
    assert len(users_db) == 1, 'Неверное количество пользователей создано в БД'


@pytest.mark.asyncio
async def test_private_message_handler():
    await broadcast.connect()
    user_gen = CombotUserDBGenerator()
    chat_gen = CombotChatDBGenerator()
    await user_gen.generate_mock_data()
    await chat_gen.generate_mock_data()

    user_db = await CombotUserDB.first()
    chat_db = await CombotChatDB.first()

    user_gen.fields['id'] = user_db.id
    chat_gen.fields['id'] = chat_db.id

    user = AsyncMock(**user_gen.fields)
    chat = AsyncMock(**chat_gen.fields)

    message = AsyncMock(**{
        'message_id': 1,
        'from_user': user,
        'chat': chat
    })

    await _handle_private_message(message)

    messages_db = await CombotMessageDB.all()

    message.answer.assert_called_with('Все сохранено')
    assert len(messages_db) == 1, 'Неверное количество сообщений создано в БД'
    await broadcast.disconnect()
