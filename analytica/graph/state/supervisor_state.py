from typing import Any, TypedDict

from ...agents.schema.agents_schema.supervisor_schema import Task


class SupervisorState(TypedDict, total=False):
    user_request: str
    objective: str
    tasks: list[Task]
    final_deliverable: str

    current_task: Task | None
    current_agent: str | None
    pending_tasks: list[Task]
    completed_tasks: list[Task]
    skipped_tasks: list[Task]

    results: dict[str, Any]
    errors: list[str]


# Alias for compatibility
AnalyticaState = SupervisorState
