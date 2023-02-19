from tortoise.contrib.pydantic import pydantic_queryset_creator, pydantic_model_creator

from telegram.communication_bot.combot_dao import CombotUserDB, CombotChatDB, CombotMessageDB


CombotUserListPydantic = pydantic_queryset_creator(
    CombotUserDB,
)
CombotChatListPydantic = pydantic_queryset_creator(
    CombotChatDB,
)
CombotMessagePydantic = pydantic_model_creator(
    CombotMessageDB,
)
