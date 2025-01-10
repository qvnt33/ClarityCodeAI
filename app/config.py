import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(filename='.env'))

OPENAI_API_KEY: str | None = os.getenv('OPENAI_API_KEY')
GITHUB_TOKEN: str | None = os.getenv('GITHUB_TOKEN')
