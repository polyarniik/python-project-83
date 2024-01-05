import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_DSN = os.getenv("DATABASE_DSN")
