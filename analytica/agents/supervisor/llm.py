from pydantic.dataclasses import dataclass

from analytica.providers.factory import ProviderFactory

from .schema import get_schema


@dataclass
class GetLLM:
    agent_name: str
    llm_provider: str

    def load_llm(self, structured=True):
        base_llm = ProviderFactory(
            provider_name=self.llm_provider, agent_name=self.agent_name
        ).get_llm()

        if not structured:
            return base_llm
        supervisor_schema = get_schema()
        return base_llm.with_structured_output(schema=supervisor_schema)
