from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    USER : str = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD : str = os.getenv("PASSWORD", "postgres")
    HOST : str = os.getenv("HOST","localhost")
    PORT : int = os.getenv("PORT",5432)
    DBNAME : str = os.getenv("DBNAME","naxadb")
    DATABASE_URL : str = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    
    class Config:
        env_file = ".env"


settings = Settings()