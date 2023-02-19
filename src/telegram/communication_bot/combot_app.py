from aiogram import Bot, Dispatcher
from aiogram.types import Update

from . import combot_api
from .combot_deps import dp, bot
from .combot_handlers import register_combot_handlers


combot_router = combot_api.router


@combot_router.on_event('startup')
async def on_startup():
    register_combot_handlers(dp)
    print('COMBOT_STARTUP')


@combot_router.post(path='/internal')
async def webhook(update: dict):
    print("BOT UPDATE")
    Dispatcher.set_current(value=dp)
    Bot.set_current(value=bot)
    await dp.process_update(update=Update(**update))

