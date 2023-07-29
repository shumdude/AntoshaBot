from asyncpg.pool import Pool


# import tortoise


# Пока что сырые запросы, нужно переделать под tortoise_orm
class Request:
    def __init__(self, connector: Pool):
        self.connector = connector

    """datausers Database"""

    async def add_datauser(self, user_id, user_name):
        query = f"""INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}') """ \
                f"""ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"""
        await self.connector.execute(query)

    """quests Database"""

    async def add_data(self, from_user, telegram_id, test, date, time, answer_time, scheduler_job_id):
        query = f"""INSERT INTO quests (from_user, telegram_id, test, date, time, answer_time, scheduler_job_id) 
                VALUES ({from_user}, {telegram_id}, '{test}', '{date}', '{time}', {answer_time}, '{scheduler_job_id}')"""
        await self.connector.execute(query)

    async def get_sender(self, job_id: str):
        query = f"""SELECT * FROM quests WHERE scheduler_job_id = '{job_id}'"""
        return await self.connector.fetchval(query)

    """catalog Database"""

    async def get_catalog(self):
        query = """SELECT * FROM catalog """
        return await self.connector.fetch(query)

    async def get_page(self, user_id: int):
        query = f"""SELECT page FROM users WHERE user_id = {user_id}"""
        return await self.connector.fetchval(query)

    async def get_product(self, offset: int):
        query = f"""SELECT * FROM catalog OFFSET {offset} LIMIT 1"""
        return await self.connector.fetchrow(query)

    async def get_catalog_length(self):
        query = """SELECT COUNT(*) FROM catalog"""
        return await self.connector.fetchval(query)

    """users Database"""

    async def add_user(self, user_id: int):
        query = f"""INSERT INTO users (user_id) VALUES ({user_id}) ON CONFLICT (user_id) DO NOTHING """
        await self.connector.execute(query)

    async def update_page(self, page: int, user_id: int):
        query = f"""UPDATE users SET page = {page} WHERE user_id = {user_id}"""
        return await self.connector.execute(query)

    # NOT DONE
    async def create_db(self):
        query = """CREATE TABLE IF NOT EXISTS test_table (id serial PRIMARY KEY,name text NOT NULL)"""
        await self.connector.execute(query)
