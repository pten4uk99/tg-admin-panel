from aiogram import Bot, Dispatcher
from aiogram.types import Update
from broadcaster import Broadcast
from fastapi import APIRouter

from src.settings import settings


# Телеграм бот
bot = Bot(token=settings.TELEGRAM_COMMUNICATION_BOT_TOKEN)
dp = Dispatcher(bot=bot)

# FastAPI роутер
router = APIRouter(
    tags=['combot'],
    prefix='/combot'
)
broadcast = Broadcast(settings.REDIS_URL)


@router.on_event('startup')
async def on_startup():
    await bot.delete_webhook()
    await bot.set_webhook(url=settings.TELEGRAM_COMMUNICATION_BOT_WEBHOOK_URL)
    await broadcast.connect()
    print('COMBOT_STARTUP')


@router.on_event('shutdown')
async def on_shutdown():
    await broadcast.disconnect()
    print('COMBOT_SHUTDOWN')



