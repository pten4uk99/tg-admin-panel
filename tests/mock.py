from admin.auth.auth_dao import AuthUserDB
from telegram.communication_bot.combot_dao import CombotUserDB, CombotChatDB
from telegram.communication_bot.combot_types import CombotChatType
from tests.generator import MockGenerator


class CombotUserDBGenerator(MockGenerator):
    fields = {
        'is_bot': False,
        'first_name': 'Katya',
        'last_name': 'Ivanova',
        'username': 'orewek',
        'language_code': 'ru_RU',
        'is_premium': False,
    }

    async def _create_object(self):
        await CombotUserDB.create(**self.fields)


class CombotChatDBGenerator(MockGenerator):
    fields = {
        'type': CombotChatType.private,
        'title': 'TestChat',
        'first_name': 'Katya',
        'last_name': 'Ivanova',
        'username': 'orewek',
        'all_members_are_administrators': False,
    }

    async def _create_object(self):
        await CombotChatDB.create(**self.fields)


class AuthUserDBGenerator(MockGenerator):
    fields = {
        'username': 'pten4uk',
        'password': '12345678',
    }

    async def _create_object(self):
        await AuthUserDB.create(**self.fields)
