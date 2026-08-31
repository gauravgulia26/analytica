from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from analytica.core.config.paths import ENV_FILE

from .config import GroqModelConfig


class GroqSetting(BaseSettings):
    config: GroqModelConfig
    groq_api_key: SecretStr

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
