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
    next_action: NextAction = Field(description="The next agent or action required.")

    task: str = Field(description="The specific task the selected agent should perform.")
