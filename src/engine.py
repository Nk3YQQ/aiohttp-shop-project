from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker


class EngineHandler:
    """ Класс для управления подключением к базу данных """

    def __init__(self, db_params: dict) -> None:
        self._driver, self._engine = db_params.get('database').split('.')
        self._database = f'{self._driver}+{self._engine}'

        self._user = db_params.get('user')
        self._password = db_params.get('password')
        self._host = db_params.get('host')
        self._port = db_params.get('port')
        self._db_name = db_params.get('db_name')

        self._url = self._create_url()
        self._engine = self._create_engine()
        self._session = self._create_async_session()

    def _create_url(self) -> str:
        return f'{self._database}://{self._user}:{self._password}@{self._host}:{self._port}/{self._db_name}'

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(self._url)

    def _create_async_session(self):
        return async_sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    def get_url(self):
        return self._url

    def get_engine(self):
        return self._engine

    def get_session(self):
        return self._session
