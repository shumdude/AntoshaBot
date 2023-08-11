from tortoise import fields, Model


class Product(Model):
    name = fields.CharField(max_length=65, pk=True)
    price = fields.BigIntField()
    url = fields.CharField(max_length=120, null=True)
    photo = fields.CharField(max_length=120, null=True)

    class Meta:
        table = "catalog"

    def __str__(self):
        return self.name


class User(Model):
    user_id = fields.BigIntField(unique=True, pk=True)
    is_admin = fields.BooleanField(default=False)
    is_private = fields.BooleanField(default=False)
    page = fields.IntField(default=1)
    phone = fields.CharField(max_length=50, null=True)
    date_of_birth = fields.DateField(null=True)
    name = fields.CharField(max_length=100, null=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.user_id


class Quest(Model):
    id = fields.BigIntField(pk=True)
    from_user = fields.BigIntField()
    telegram_id = fields.BigIntField()
    test = fields.CharField(max_length=1000)
    date = fields.CharField(max_length=100)
    time = fields.CharField(max_length=100)
    answer_time = fields.BigIntField()
    scheduler_job_id = fields.CharField(max_length=1000)

    class Meta:
        table = "quests"

    def __str__(self):
        return self.test
