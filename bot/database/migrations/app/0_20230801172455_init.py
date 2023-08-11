from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "catalog" (
    "name" VARCHAR(65) NOT NULL  PRIMARY KEY,
    "price" BIGINT NOT NULL,
    "url" VARCHAR(120),
    "photo" VARCHAR(120)
);
CREATE TABLE IF NOT EXISTS "quests" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "from_user" BIGINT NOT NULL,
    "telegram_id" BIGINT NOT NULL,
    "test" VARCHAR(1000) NOT NULL,
    "date" VARCHAR(100) NOT NULL,
    "time" VARCHAR(100) NOT NULL,
    "answer_time" BIGINT NOT NULL,
    "scheduler_job_id" VARCHAR(1000) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "user_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_private" BOOL NOT NULL  DEFAULT False,
    "page" INT NOT NULL  DEFAULT 1,
    "phone" VARCHAR(50),
    "date_of_birth" DATE,
    "name" VARCHAR(100)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
