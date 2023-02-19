from tortoise import models, fields


class AuthUserDB(models.Model):
    """ Администратор, который общается с пользователем через бота """

    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=1024, unique=True)
    password = fields.CharField(max_length=1024)


class AuthTokenDB(models.Model):
    """ Токен авторизации администратора """

    user = fields.ForeignKeyField('models.AuthUserDB')
    key = fields.CharField(max_length=32, unique=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
