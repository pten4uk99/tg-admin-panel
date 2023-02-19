from aiogram import types, Dispatcher

from telegram.communication_bot.combot_services import register_tg_user, register_message


async def _handle_start_command(message: types.Message):
    """ Обрабатывает команду /start """

    await register_tg_user(message)
    await message.answer(f'Здравствуйте {message.from_user.username}! Вы успешно зарегистрированы.')


async def _handle_help_command(message: types.Message):
    """ Обрабатывает комманду /help """

    await message.answer('Бот подддержки. Описание пока что отсутствует.')


async def _handle_private_message(message: types.Message):
    """ Обрабатывает сообщение от пользователя в приватный чат с ботом """

    await register_message(message)
    await message.answer('Все сохранено')


def register_combot_handlers(dp: Dispatcher):
    dp.register_message_handler(_handle_start_command, commands=['start'])
    dp.register_message_handler(_handle_help_command, commands=['help'])
    dp.register_message_handler(_handle_private_message)
