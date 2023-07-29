from tortoise import fields, Model


class FieldsMixin:
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Catalog(Model, FieldsMixin):
    name = fields.CharField(max_length=65)
    price = fields.BigIntField()
    url = fields.CharField(max_length=120, null=True)
    photo = fields.CharField(max_length=120, null=True)


class Users(Model, FieldsMixin):
    user_id = fields.BigIntField(unique=True)
    is_admin = fields.BooleanField(default=False)
    is_private = fields.BooleanField(default=False)
    page = fields.IntField(default=1)

# class User(Model, FieldsMixin):
#     tg_id = fields.BigIntField(unique=True)
#     first_name = fields.CharField(max_length=65)
#     last_name = fields.CharField(max_length=65, null=True)
#     tg_username = fields.CharField(max_length=65, null=True)
#     password = fields.CharField(max_length=120, null=True)
#     is_admin = fields.BooleanField(default=False)