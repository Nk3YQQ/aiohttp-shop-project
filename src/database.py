import os

from dotenv import load_dotenv

from src.engine import EngineHandler

load_dotenv()

DATABASE_PARAMS = {
    'database': 'postgresql.asyncpg',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', '5432'),
    'db_name': os.getenv('DB_NAME')
}

engine_handler = EngineHandler(DATABASE_PARAMS)

database_url = engine_handler.get_url()

engine = engine_handler.get_engine()

async_session = engine_handler.get_session()
