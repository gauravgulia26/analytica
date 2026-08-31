from langchain_groq import ChatGroq
from pydantic.dataclasses import dataclass

from analytica.core.config.paths import DEFAULT_CONFIG_PATH
from analytica.utils.loaders import load_yaml_key

from ..groq.settings import GroqModelConfig, GroqSetting
from ..registry import AVAILAIBLE_PROVIDERS


def list_providers():
    return " ".join(AVAILAIBLE_PROVIDERS)


@dataclass
class ProviderFactory:
    provider_name: str
    agent_name: str

    def __post_init__(self):
        if self.provider_name not in AVAILAIBLE_PROVIDERS:
            raise NotImplementedError(f"{self.provider_name} is not registered yet.")

    def __load_params(self) -> dict:
        params = load_yaml_key(file_path=DEFAULT_CONFIG_PATH, key=self.provider_name)["agents"][
            self.agent_name
        ]
        return params

    def __load_settings(self):
        match self.provider_name:
            case "groq":
                return GroqSetting(config=GroqModelConfig(**(self.__load_params())))

    def get_llm(self) -> ChatGroq:

        cfg = self.__load_settings()

        return ChatGroq(
            model=cfg.config.model,
            temperature=cfg.config.temperature,
            max_tokens=cfg.config.max_tokens,
            max_retries=cfg.config.max_retries,
            api_key=cfg.groq_api_key.get_secret_value(),
        )
