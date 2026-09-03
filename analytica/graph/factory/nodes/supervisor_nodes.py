from time import sleep
from typing import Any

from groq import BadRequestError
from langchain_core.runnables import Runnable
from rich import print

from ....agents.schema.agents_schema.supervisor_schema import SupervisorOutput
from ...state.supervisor_state import SupervisorState


class SupervisorNodes:
    """
    Node executor for the Supervisor Agent.
    """

    def __init__(
        self,
        agent_chain: Runnable,
        agent_input_variable: list[str],
        agent_name: str = "supervisor_agent",
    ):
        self.agent_chain = agent_chain
        self.agent_input_variable = agent_input_variable
        self.agent_name = agent_name

    def invoke_with_retry(
        self,
        chain: Runnable,
        inputs: dict[str, Any],
        max_attempts: int = 3,
    ) -> Any:
        for attempt in range(1, max_attempts + 1):
            try:
                return chain.invoke(inputs)
            except BadRequestError as e:
                if attempt == max_attempts:
                    raise
                print(
                    f"[yellow]Attempt {attempt} failed: {e}. "
                    f"Retrying... ({attempt + 1}/{max_attempts})[/yellow]"
                )
                sleep(1)

    def get_supervisor_response(self, state: SupervisorState) -> dict[str, Any]:
        """
        Execute the supervisor agent chain to decompose user_request into structured tasks.
        """
        response: SupervisorOutput = self.invoke_with_retry(
            chain=self.agent_chain,
            inputs={self.agent_input_variable[0]: state["user_request"]},
            max_attempts=3,
        )

        return {
            "objective": response.objective,
            "tasks": response.tasks,
            "pending_tasks": response.tasks,
            "completed_tasks": [],
            "final_deliverable": response.final_deliverable,
        }
