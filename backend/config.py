import os
from re import compile as comp
from re import Pattern
from dotenv import load_dotenv


load_dotenv()



class Config:
    def __init__(self):
        self.patterns = [
            comp(
                r"jdbc:postgresql://(?P<host>[\w\.-]+):(?P<port>\d+)/(?P<database>[\w\-]+)\?currentSchema=(?P<currentSchema>\w+)"
            ),
            comp(
                r"jdbc:postgresql://(?P<host>[\w\.-]+):(?P<port>\d+)/(?P<database>[\w\-]+)"
            ),
            comp(
                r"jdbc:postgresql://(?P<user>\w+):(?P<password>[^\/]+)@(?P<host>[\w\.-]+):(?P<port>\d+)/(?P<database>[\w\-]+)\?currentSchema=(?P<currentSchema>\w+)"
            ),
            comp(
                r"jdbc:postgresql://(?P<user>\w+):(?P<password>[^\/]+)@(?P<host>[\w\.-]+):(?P<port>\d+)/(?P<database>[\w\-]+)"
            ),
        ]
        # получение строки конфигурации для бд с пациентами
        self.JDBC_STRING = os.environ.get("mainpool.jdbcString", '')
        # проверка на то что она есть 
        if not self.JDBC_STRING:
            raise Exception("No jdbc string provided")

        # парсим конфиг строку
        params = self.parse_jdbc_string(self.JDBC_STRING, self.patterns)
        self.DB_HOST = params.get("host")
        self.DB_PORT = params.get("port")
        self.DB_NAME = params.get("database")
        self.DB_USER = params.get("user", os.environ.get("mainpool.jdbcUser", ""))
        if not self.DB_USER:
            raise Exception("No user provided")
        self.DB_PASSWORD = params.get(
            "password", os.environ.get("mainpool.jdbcPassword", "")
        )
        if not self.DB_PASSWORD:
            raise Exception("No password provided")

        self.DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



        self.JDBC_STRING_PDF = os.environ.get("storagepool.jdbcString", '')
        if not self.JDBC_STRING_PDF:
            raise Exception("No jdbc string provided")
        params = self.parse_jdbc_string(self.JDBC_STRING_PDF, self.patterns)
        self.DB_HOST_PDF = params.get("host")
        self.DB_PORT_PDF = params.get("port")
        self.DB_NAME_PDF = params.get("database")
        self.TABLE_SCHEMA_PDF = params.get('currentSchema')
        self.TABLE_NAME_PDF = 'pdf_mdoc'
        self.DB_USER_PDF = params.get("user", os.environ.get("storagepool.jdbcUser", ""))
        if not self.DB_USER_PDF:
            raise Exception("No user provided")
        self.DB_PASSWORD_PDF = params.get(
            "password", os.environ.get("storagepool.jdbcPassword", "")
        )
        if not self.DB_PASSWORD_PDF:
            raise Exception("No password provided")

        self.DATABASE_URL_PDF = f"postgresql+asyncpg://{self.DB_USER_PDF}:{self.DB_PASSWORD_PDF}@{self.DB_HOST_PDF}:{self.DB_PORT_PDF}/{self.DB_NAME_PDF}"

        self.REDIS_DB = os.environ.get("spring.redis.database", str)
        self.REDIS_HOST = os.environ.get("spring.redis.host", str)
        self.REDIS_PORT = os.environ.get("spring.redis.port", int)
        self.REDIS_PASSWORD = os.environ.get("spring.redis.password", str)
        self.REDIS_TIMEOUT = os.environ.get("spring.redis.timeout") or 3000


        self.REDIS_SENTINEL_HOST = os.environ.get("spring.redis.sentinel.host", str)
        self.REDIS_SENTINEL_MASTER = os.environ.get("spring.redis.sentinel.master", str)
        self.REDIS_SENTINEL_PASSWORD = os.environ.get("spring.redis.sentinel.password", str)
        self.REDIS_SENTINEL_PORT = os.environ.get("spring.redis.sentinel.port", int)

        self.SESSION_TIME = os.environ.get("SESSION_TIME") or 3600






    def parse_jdbc_string(self, jdbc: str, pat: list[Pattern[str]] = None) -> dict:
        """
        Парсит строку подключения JDBC и возвращает параметры подключения.

        -- Args:
            - **jdbc** (str, optional): Строка подключения JDBC.
            - **pat** (list[Pattern[str]], optional): Список паттернов для поиска параметров подключения.

        -- Returns:
            - dict: Параметры подключения.

        -- Usage:
            params = db_manager.parse_jdbc_string()
        """

        for pattern in pat:
            match = pattern.match(jdbc)
            if match:
                db_params = match.groupdict()
                return db_params


# class Config:
#    DB_HOST = os.getenv("DB_HOST")
#    DB_PORT = os.getenv("DB_PORT")
#    DB_USER = os.getenv("mainpool.jdbcUser")
#    DB_PASSWORD = os.getenv("mainpool.jdbcPassword")
#    DB_NAME = os.getenv("DB_NAME")
#    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#
#    DB_HOST_PDF = os.getenv("DB_HOST_PDF")
#    DB_PORT_PDF = os.getenv("DB_PORT_PDF")
#    DB_USER_PDF = os.getenv("spring.datasource.username")
#    DB_PASSWORD_PDF = os.getenv("storage-password")
#    DB_NAME_PDF = os.getenv("DB_NAME_PDF")
#    TABLE_NAME_PDF = os.getenv('TABLE_NAME_PDF')
#    TABLE_SCHEMA_PDF = os.getenv('TABLE_SCHEMA_PDF')
#    DATABASE_URL_PDF = f"postgresql+asyncpg://{DB_USER_PDF}:{DB_PASSWORD_PDF}@{DB_HOST_PDF}:{DB_PORT_PDF}/{DB_NAME_PDF}"
#
#
#    def parse_jdbc_string(self, jdbc: str = None, pat: list[Pattern[str]] = None):
#        """
#        Парсит строку подключения JDBC и возвращает параметры подключения.
#
#        -- Args:
#            - **jdbc** (str, optional): Строка подключения JDBC.
#            - **pat** (list[Pattern[str]], optional): Список паттернов для поиска параметров подключения.
#
#        -- Returns:
#            - dict: Параметры подключения.
#
#        -- Usage:
#            params = db_manager.parse_jdbc_string()
#        """
#
#        if not jdbc:
#            jdbc = self.param.jdbc_string
#            pat = self.param.patterns
#
#        if jdbc:
#            for pattern in pat:
#                match = pattern.match(jdbc)
#                if match:
#                    db_params = match.groupdict()
#                    if 'user' not in db_params or 'password' not in db_params:
#                        db_params.update({'user': self.param.db_user, 'password': self.param.db_password})
#                    return db_params
#        else:
#            return self.config_db()
#

config = Config()
