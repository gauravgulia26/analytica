from langchain_core.runnables import Runnable
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from ...state.supervisor_state import SupervisorState


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class SupervisorNodes:
    agent_chain: Runnable
    agent_input_variable: list[str]
    agent_name: str = "supervisor_agent"

    def get_supervisor_response(self, state: SupervisorState):
        user_query = state["user_request"]
        response = self.agent_chain.invoke({self.agent_input_variable[0]: user_query})
        return {"tasks": response.agent_flow}
