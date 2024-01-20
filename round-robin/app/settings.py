from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Number of instance in the queue
    NO_INSTANCES: int

    class Config:
        env_file = ".env"
