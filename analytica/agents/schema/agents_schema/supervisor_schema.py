from enum import Enum

from pydantic import BaseModel, Field


class NextAction(str, Enum):
    DATA_ANALYSIS = "data_analysis"
    STATISTICAL_ANALYSIS = "statistical_analysis"
    PYTHON_ANALYSIS = "python_analysis"
    VISUALIZATION = "visualization"
    VALIDATION = "validation"
    INSIGHT = "insight"
    REPORT = "report"
    END = "end"


class SupervisorOutput(BaseModel):
    agent_flow: list[NextAction] = Field(
        title="The next agent or action required.",
        description="The list of the agents in the same order they needs to be executed based on the user request",
        examples=[NextAction.DATA_ANALYSIS, NextAction.STATISTICAL_ANALYSIS],
        alias="flow",
    )
    reasoning: dict[NextAction, str] = Field(
        title="Reasoning behind the selected agent.",
        description="Reasoning behind selecting each agent, why it is selected and why it is needed for the flow. Refer user query for this, what you find in user query that made you select this agent.",
        examples=[
            {
                NextAction.DATA_ANALYSIS: "User requested data analysis from the query",
                NextAction.STATISTICAL_ANALYSIS: "Statistical agent needs for the workflow to run smoothly",
            }
        ],
    )
