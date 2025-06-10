import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(DATABASE_URL)

    DB_HOST_PDF = os.getenv("DB_HOST")
    DB_PORT_PDF = os.getenv("DB_PORT")
    DB_USER_PDF = os.getenv("DB_USER")
    DB_PASSWORD_PDF = os.getenv("DB_PASSWORD")
    DB_NAME_PDF = os.getenv("DB_NAME")
    DATABASE_URL_PDF = f"postgresql+asyncpg://{DB_USER_PDF}:{DB_PASSWORD_PDF}@{DB_HOST_PDF}:{DB_PORT_PDF}/{DB_NAME_PDF}"

    SSH_USER = os.getenv("SSH_USER")
    SSH_PASSWORD = os.getenv("SSH_PASSWORD")
    BASE_COMMAND = os.getenv("BASE_COMMAND")


config = Config()

