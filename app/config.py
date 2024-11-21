from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432)) 
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "naxadb")         
    
    DATABASE_URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings()
