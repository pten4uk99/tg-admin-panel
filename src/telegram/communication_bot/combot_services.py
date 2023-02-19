from starlette.websockets import WebSocket
from tortoise.models import QuerySet
from aiogram import types

from telegram.communication_bot.combot_dao import CombotUserDB, CombotChatDB, CombotMessageDB
from telegram.communication_bot.combot_deps import broadcast
from telegram.communication_bot.combot_utils import get_ws_room_name


async def register_tg_user(message: types.Message):
    """ Создает/обновляет пользователя и чат в БД на основе message """

    await CombotUserDB.update_or_create(**message.from_user.to_python())
    await CombotChatDB.update_or_create(**message.chat.to_python())


async def register_message(message: types.Message):
    """ Создает сообщение в БД """

    user = await CombotUserDB.get(id=message.from_user.id)
    chat = await CombotChatDB.get(id=message.chat.id)

    await CombotMessageDB.create(
        user=user,
        chat=chat,
        text=message.text
    )


async def send_message_from_bot(message: str, chat: types.Chat):
    """ Отправляет сообщение в чат от лица бота """

    pass


async def find_users(**filters):
    """ Возвращает список объектов с фильтрами filters """

    if filters is None:
        filters = {}

    return CombotUserDB.filter(**filters)


async def find_user_by_id(pk: int):
    """ Возвращает конкретный объект из БД """

    return CombotUserDB.filter(id=pk)


async def find_chats(**filters):
    """ Возвращает список объектов с фильтрами filters """

    if filters is None:
        filters = {}

    return CombotChatDB.filter(**filters)


async def find_chat_by_id(pk: int):
    """ Возвращает конкретный объект из БД """

    return CombotChatDB.filter(id=pk)


async def find_chat_by_user_id(user_id: int):
    """ Возвращает чат по идентификатору пользователя """

    chat = await CombotChatDB.filter(combotmessagedbs__user__id=user_id).first()
    return chat


async def chatroom_ws_sender(websocket: WebSocket, chat_id: int):
    async with broadcast.subscribe(channel=get_ws_room_name(chat_id)) as subscriber:
        async for event in subscriber:
            await websocket.send_json(data=event.message)


# async def chatroom_ws_receiver(websocket: WebSocket, user_id: int):
#     async for message in websocket.iter_text():
#         await broadcast.publish(channel=get_ws_room_name(user_id), message=message)
