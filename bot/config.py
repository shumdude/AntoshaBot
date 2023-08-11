from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    host: str  # URL-адрес базы данных
    port: str  # Порт базы данных
    user: str  # Username пользователя базы данных
    password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig

    def db_url(self) -> str:
        return f"asyncpg://{self.db.user}:{self.db.password}@{self.db.host}:{self.db.port}/{self.db.database}"


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DatabaseConfig(database=env('POSTGRES_DB'),
                                    host=env('POSTGRES_HOST'),
                                    port=env('POSTGRES_PORT'),
                                    user=env('POSTGRES_USER'),
                                    password=env('POSTGRES_PASSWORD')))


config: Config = load_config('.env')
TORTOISE_ORM = {
    'connections': {'default': config.db_url()},
    'apps': {
        'app': {
            'models': ['bot.database.models', 'aerich.models'],
            'default_connection': 'default'
        },
    },
}
