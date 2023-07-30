from tortoise import fields, Model


class Catalog(Model):
    name = fields.CharField(max_length=65, pk=True)
    price = fields.BigIntField()
    url = fields.CharField(max_length=120, null=True)
    photo = fields.CharField(max_length=120, null=True)

    class Meta:
        table = "catalog"

    def __str__(self):
        return self.name


class Users(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    is_admin = fields.BooleanField(default=False)
    is_private = fields.BooleanField(default=False)
    page = fields.IntField(default=1)

    class Meta:
        table = "users"

    def __str__(self):
        return self.user_id
