from telegram.communication_bot.combot_types import AvailableChannels


def get_ws_room_name(chat_id: int) -> str:
    return f'{AvailableChannels.COMMUNICATION_BOT_CHAT.value}_{chat_id}'

