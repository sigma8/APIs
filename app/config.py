from pydantic import BaseSettings

class Settings(BaseSettings):
    #database settings
    DB_HOSTNAME: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    #token
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()