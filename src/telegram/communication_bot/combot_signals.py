from typing import Type

from tortoise import signals

from telegram.communication_bot.combot_dao import CombotMessageDB
from telegram.communication_bot.combot_deps import broadcast
from telegram.communication_bot.combot_models import CombotMessagePydantic
from telegram.communication_bot.combot_utils import get_ws_room_name


@signals.post_save(CombotMessageDB)
async def new_message(sender: Type[CombotMessageDB], obj: CombotMessageDB, created: bool, *args):
    pydantic_message = CombotMessagePydantic.from_orm(obj)
    chat = await obj.chat
    await broadcast.publish(channel=get_ws_room_name(chat.id), message=pydantic_message.json())
