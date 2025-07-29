import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("mainpool.jdbcUser")
    DB_PASSWORD = os.getenv("mainpool.jdbcPassword")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DB_HOST_PDF = os.getenv("DB_HOST_PDF")
    DB_PORT_PDF = os.getenv("DB_PORT_PDF")
    DB_USER_PDF = os.getenv("spring.datasource.username")
    DB_PASSWORD_PDF = os.getenv("storage-password")
    DB_NAME_PDF = os.getenv("DB_NAME_PDF")
    TABLE_NAME_PDF = os.getenv('TABLE_NAME_PDF')
    TABLE_SCHEMA_PDF = os.getenv('TABLE_SCHEMA_PDF')
    DATABASE_URL_PDF = f"postgresql+asyncpg://{DB_USER_PDF}:{DB_PASSWORD_PDF}@{DB_HOST_PDF}:{DB_PORT_PDF}/{DB_NAME_PDF}"

    DB_HOST_GROUP_DOC = os.getenv('DB_HOST_GROUP_DOC')
    DB_PORT_GROUP_DOC = os.getenv('DB_PORT_GROUP_DOC')
    DB_USER_GROUP_DOC = os.getenv('DB_USER_GROUP_DOC')
    DB_PASSWORD_GROUP_DOC = os.getenv('DB_PASSWORD_GROUP_DOC')
    DB_NAME_GROUP_DOC = os.getenv('DB_NAME_GROUP_DOC')
    DATABASE_URL_GROUP_DOC = f"postgresql+asyncpg://{DB_USER_GROUP_DOC}:{DB_PASSWORD_GROUP_DOC}@{DB_HOST_GROUP_DOC}:{DB_PORT_GROUP_DOC}/{DB_NAME_GROUP_DOC}"


config = Config()

