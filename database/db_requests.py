from .models import User, Product, Quest
# from tortoise import connections


class DBRequest:
    # def __init__(self, connector: Pool):
    #     self.connector = connector

    """quests Database"""

    async def add_data(self, from_user, telegram_id, test, date, time, answer_time, scheduler_job_id):
        return await Quest.create(from_user=from_user,
                                  telegram_id=telegram_id,
                                  test=test, date=date, time=time,
                                  answer_time=answer_time,
                                  scheduler_job_id=scheduler_job_id)

    async def get_sender(self, job_id: str):
        return await Quest.get_or_none(scheduler_job_id=job_id).values_list("from_user", flat=True)

    """catalog Database"""

    async def get_catalog(self):
        return await Product.all()

    async def get_product(self, offset: int):
        return await Product.all().offset(offset).limit(1).first()

    async def get_catalog_length(self):
        return await Product.all().count()

    """users Database"""

    async def add_user(self, user_id: int):
        # query = f"""INSERT INTO users (user_id) VALUES ({user_id}) ON CONFLICT (user_id) DO NOTHING """
        # conn = connections.get("default")
        # await conn.execute_query(query)
        await User.update_or_create(user_id=user_id)

    async def update_page(self, page: int, user_id: int):
        return await User.filter(user_id=user_id).update(page=page)

    async def get_page(self, user_id: int):
        return await User.get_or_none(user_id=user_id).values_list("page", flat=True)

    async def registration(self, user_id: int, name: str, date_of_birth: str, phone: str):
        return await User.filter(user_id=user_id).update(name=name, date_of_birth=date_of_birth, phone=phone)

    async def get_user(self, user_id: int):
        return await User.get_or_none(user_id=user_id)

    """NOT DONE"""
    # query = """CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY,name text NOT NULL)"""
    # query = f"""INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}') """ \
    #         f"""ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"""
