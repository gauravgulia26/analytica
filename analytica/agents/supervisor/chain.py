from langchain_core.runnables import Runnable

from ..common.utils import make_prompt_template
from .llm import GetLLM


def load_supervisor_chain() -> Runnable:
    supervisor_prompt = make_prompt_template(
        prompt_name="supervisor_prompt", input_variables=["user_query"]
    )
    supervisor_llm = GetLLM(agent_name="supervisor_agent", llm_provider="groq").load_llm()

    return supervisor_prompt | supervisor_llm
