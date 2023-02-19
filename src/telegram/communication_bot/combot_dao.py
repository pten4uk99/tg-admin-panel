from tortoise import models, fields

from telegram.communication_bot.combot_types import CombotChatType


class CombotUserDB(models.Model):
    """
    Модель пользователя, который общается с ботом.
    """

    id = fields.BigIntField(pk=True)
    is_bot = fields.BooleanField(null=True)
    first_name = fields.CharField(max_length=1024, null=True)
    last_name = fields.CharField(max_length=1024, null=True)
    username = fields.CharField(max_length=1024, null=True)
    language_code = fields.CharField(max_length=8)
    is_premium = fields.BooleanField(null=True)


class CombotChatDB(models.Model):
    """
    Модель чата между пользователем и ботом.
    """

    id = fields.BigIntField(pk=True)
    type = fields.CharEnumField(enum_type=CombotChatType, max_length=1024)
    title = fields.CharField(max_length=1024, null=True)
    first_name = fields.CharField(max_length=1024, null=True)
    last_name = fields.CharField(max_length=1024, null=True)
    username = fields.CharField(max_length=1024, null=True)
    all_members_are_administrators = fields.BooleanField(default=False)


class CombotMessageDB(models.Model):
    """
    Модель сообщения в чате между пользователем и ботом.
    """

    id = fields.BigIntField(pk=True)
    # null потому что у сообщения может не быть пользователя (если отправляет администратор от лица бота)
    user = fields.ForeignKeyField(f'models.CombotUserDB', on_delete=fields.CASCADE, null=True)
    chat = fields.ForeignKeyField(f'models.CombotChatDB', on_delete=fields.CASCADE)
    datetime = fields.DatetimeField(auto_now_add=True)
    text = fields.TextField()
