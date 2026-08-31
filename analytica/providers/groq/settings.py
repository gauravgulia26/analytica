"""
Settings and environment configuration loader for the Groq provider.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from analytica.core.config.paths import ENV_FILE

from .config import GroqModelConfig


class GroqSetting(BaseSettings):
    """
    Application settings for Groq LLM integration, managing credentials and model configuration.

    Attributes:
        config: Model parameters configuration object.
        groq_api_key: Secret API key for Groq authentication (loaded from environment).
    """

    config: GroqModelConfig
    groq_api_key: SecretStr

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
