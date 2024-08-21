from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    host: str
    user: str
    password: str
    db_name: str
    port: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        host=env('HOST'),
        user=env('USER'),
        password=env('PASSWORD'),
        db_name=env('DB_NAME'),
        port=env('PORT')
    )
