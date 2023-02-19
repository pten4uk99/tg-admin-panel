from starlette.websockets import WebSocket
from fastapi import HTTPException, WebSocketException

from telegram.communication_bot.combot_deps import router
from telegram.communication_bot.combot_models import CombotUserListPydantic, CombotChatListPydantic
from telegram.communication_bot.combot_services import find_users, find_user_by_id, find_chats, \
    find_chat_by_id, chatroom_ws_sender, find_chat_by_user_id


@router.get('/users', response_model=CombotUserListPydantic, summary='Список всех пользователей')
async def get_users():
    """ Получение списка пользователей """

    users = await find_users()
    return await CombotUserListPydantic.from_queryset(users)


@router.get('/users/{user_id}', response_model=CombotUserListPydantic, summary='Конкретный пользователь')
async def get_user_by_id(user_id: int):
    """ Получение конкретного пользователя по идентификатору """

    user = await find_user_by_id(pk=user_id)
    return await CombotUserListPydantic.from_queryset(user)


@router.get('/chats', response_model=CombotChatListPydantic, summary='Список всех чатов')
async def get_chats():
    """ Получение списка всех чатов """

    chats = await find_chats()
    return await CombotChatListPydantic.from_queryset(chats)


@router.get('/chats/{chat_id}', response_model=CombotChatListPydantic, summary='Конкретный чат')
async def get_chat_by_id(chat_id: int):
    """ Получение конкретного чата по идентификатору """

    chat = await find_chat_by_id(pk=chat_id)
    return await CombotChatListPydantic.from_queryset(chat)




