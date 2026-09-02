import sys

from langchain.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from pydantic import BaseModel, ConfigDict
from pydantic.errors import PydanticSchemaGenerationError

from analytica.agents.common.utils import make_prompt_template
from analytica.exception import AnalyticaException
from analytica.providers.factory import ProviderFactory


class AgentBuilder(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    agent_name: str
    agent_prompt_name: str
    agent_input_variables: list[str]
    agent_provider: str
    agent_schema: type[BaseModel]

    @property
    def __prompt(self) -> Runnable:
        try:
            chat_prompt = make_prompt_template(
                prompt_name=self.agent_prompt_name,
                input_variables=self.agent_input_variables,
            )
        except FileNotFoundError as e:
            raise AnalyticaException(error=e, error_detail=sys)
        except PydanticSchemaGenerationError as e:
            raise AnalyticaException(error=e, error_detail=sys)
        else:
            return chat_prompt

    @property
    def llm(self) -> BaseChatModel:
        base_llm = ProviderFactory(
            provider_name=self.agent_provider, agent_name=self.agent_name
        ).get_llm()

        return base_llm.with_structured_output(self.agent_schema)

    @property
    def get_config_grid(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "agent_provider": self.agent_provider,
            "agent_llm": self.llm,
            "agent_input_variables": self.agent_input_variables,
            "agent_prompt_name": self.agent_prompt_name,
        }

    @property
    def get_prompt(self) -> Runnable:
        return self.__prompt

    @property
    def get_schema(self) -> dict:
        return self.agent_schema.model_json_schema()

    def build_agent_chain(self) -> Runnable:
        return self.__prompt | self.llm
