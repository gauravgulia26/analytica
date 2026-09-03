"""
Factory module for instantiating LLM chat model clients based on provider and agent configuration.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq
from pydantic.dataclasses import dataclass

from analytica.core.config.paths import DEFAULT_CONFIG_PATH
from analytica.utils.loaders import load_yaml_key

from ..groq.settings import GroqModelConfig, GroqSetting
from ..registry import AVAILAIBLE_PROVIDERS


def list_providers() -> str:
    """
    List all supported LLM providers as a space-separated string.

    Returns:
        str: Space-separated names of available providers.
    """
    return " ".join(AVAILAIBLE_PROVIDERS)


@dataclass
class ProviderFactory:
    """
    Factory responsible for loading agent-specific provider configuration and
    creating LLM instances.

    Attributes:
        provider_name: The name of the LLM provider (e.g., 'groq').
        agent_name: The name of the agent whose configuration should be loaded.
    """

    provider_name: str
    agent_name: str

    def __post_init__(self) -> None:
        """
        Validate that the requested provider is supported in the registry.

        Raises:
            NotImplementedError: If provider_name is not found in AVAILAIBLE_PROVIDERS.
        """
        if self.provider_name not in AVAILAIBLE_PROVIDERS:
            raise NotImplementedError(f"{self.provider_name} is not registered yet.")

    def __load_params(self) -> dict:
        """
        Load agent-specific configuration parameters from the provider YAML configuration file.

        Returns:
            dict: Configuration dictionary for the specified agent.
        """
        provider_config = load_yaml_key(
            file_path=DEFAULT_CONFIG_PATH,
            key=self.provider_name,
        )

        return provider_config["agents"][self.agent_name]

    def __load_settings(self):
        """
        Construct the provider-specific settings object populated with loaded model parameters.

        Returns:
            GroqSetting: Initialized provider settings instance.
        """
        match self.provider_name:
            case "groq":
                return GroqSetting(config=GroqModelConfig(**(self.__load_params())))

    def get_llm(self) -> BaseChatModel:
        """
        Instantiate and return the configured LangChain chat model.

        Returns:
            BaseChatModel: Ready-to-use LangChain chat model instance (e.g., ChatGroq).
        """
        cfg = self.__load_settings()

        return ChatGroq(
            model=cfg.config.model,
            temperature=cfg.config.temperature,
            max_tokens=cfg.config.max_tokens or 32768,
            max_retries=cfg.config.max_retries,
            reasoning_effort=cfg.config.reasoning_efforts,
            api_key=cfg.groq_api_key.get_secret_value(),
        )
