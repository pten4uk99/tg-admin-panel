from enum import Enum


class CombotChatType(str, Enum):
    private = 'private'
    group = 'group'


class AvailableChannels(str, Enum):
    COMMUNICATION_BOT_CHAT = 'communication_bot_chat'
