from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Number of instance in the queue
    NO_INSTANCES: int
    INSTANCE_PREFIX: str

    class Config:
        env_file = ".env"
