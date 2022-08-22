from datetime import timedelta

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


def build_dsn(
        protocol: str,
        user: str,
        password: str,
        host: str,
        port: int,
        path: str,
) -> str:
    return f'{protocol}://postgres:{password}@{host}:{port}/{path}'


class DatabaseSettings(BaseSettings):
    protocol: str = 'postgresql'
    user: str = 'postgres'
    password: str = '123qwe'
    host: str = 'db'
    port: int = 5432
    name: str = 'auth_database'

    @property
    def dsn(self) -> str:
        return build_dsn(
            protocol=self.protocol,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class RedisSettings(BaseSettings):
    host: str = 'storage'
    port: int = 6379


class JWTSettings(BaseSettings):
    access_token_expire_time: timedelta = timedelta(minutes=1)
    refresh_token_expire_time: timedelta = timedelta(days=7)
    token_location = ['headers', 'query_string']
    secret_key: str = 'DEBUG'


class WSGISettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5000
    workers: int = 4


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()
    wsgi: WSGISettings = WSGISettings()


settings = Settings()
