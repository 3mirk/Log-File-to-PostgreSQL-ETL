import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_port: str = os.getenv("DB_PORT", "5432")
    db_name: str = os.getenv("DB_NAME", "che_dvi_track")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    monitored_folder: str = os.getenv("MONITORED_FOLDER", r"I:\VISION\LDS\jobrte")
    file_settle_seconds: float = float(os.getenv("FILE_SETTLE_SECONDS", "1"))


settings = Settings()
