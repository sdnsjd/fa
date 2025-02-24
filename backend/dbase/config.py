from dotenv import load_dotenv
import os
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path)
DATABASE_URL_asyncpg = os.getenv('DATABASE_URL_asyncpg')
