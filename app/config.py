from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'


settings = Settings()