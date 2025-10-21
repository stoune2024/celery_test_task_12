from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    SMTP_LOGIN: EmailStr
    SMTP_PASSWORD: str
    SMTP_PASSWORD_FOR_APP: str
    SMTP_HOST: str

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env"
    )


settings = Settings()


@lru_cache()
def get_settings():
    return settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
