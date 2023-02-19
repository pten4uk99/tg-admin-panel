import logging
import sys

from pydantic import BaseSettings


fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("db_client")
logger_db_client.setLevel(logging.INFO)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.INFO)
logger_tortoise.addHandler(sh)


class Settings(BaseSettings):
    DATABASE_URL: str
    # DATABASE_URL = f'postgres://postgres:admin@localhost:5432/test'
    REDIS_URL: str
    TELEGRAM_COMMUNICATION_BOT_TOKEN: str
    TELEGRAM_COMMUNICATION_BOT_WEBHOOK_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PROXY_PREFIX: str

    class Config:
        env_file = "env/dev.env"
        env_file_encoding = "utf-8"


settings = Settings()


# aerich миграции для tortoise
# TORTOISE_ORM = {
#     "connections": {"default": DATABASE_URL},
#     "apps": {
#         "models": {
#             "models": [
#                 'app.chat.chat_models',
#             ],
#             "default_connection": "default",
#         },
#     },
# }
