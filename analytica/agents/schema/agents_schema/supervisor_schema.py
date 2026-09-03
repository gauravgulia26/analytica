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


class Task(BaseModel):
    task_id: str = Field(description="Unique task identifier, e.g. 'task_1', 'task_2'")
    action: NextAction = Field(
        description="The specialized capability/action needed for this task"
    )
    objective: str = Field(description="Clear, specific objective of this analytical task")
    description: str = Field(
        description="Scope and instructions for the task, explaining what needs to be performed",
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="List of task_ids that must be completed before this task can start",
    )
    expected_output: list[str] = Field(
        default_factory=list,
        description="Key output deliverables or findings expected from this task",
    )


class SupervisorOutput(BaseModel):
    objective: str = Field(
        description="The overall objective of the requested analytical workflow."
    )

    tasks: list[Task] = Field(
        description="Ordered list of tasks required to complete the workflow."
    )

    final_deliverable: str = Field(
        description="The final result that should be delivered to the user."
    )
