from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "绝缘材料参数工具"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_HOST: str = "47.116.114.44"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "A123456z"
    DATABASE_NAME: str = "shujiao"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    ALLOWED_ORIGINS: List[AnyHttpUrl] = []

    # WeChat Mini Program
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""

    # WeChat Payment
    WECHAT_MCH_ID: str = ""
    WECHAT_MCH_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
