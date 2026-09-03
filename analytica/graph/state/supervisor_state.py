from enum import Enum
from typing import Any, TypedDict


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SupervisorState(TypedDict):
    user_request: str

    tasks: list[Any]

    current_task: str | None
    current_agent: str | None
    pending_tasks: list[Any]
    skipped_tasks: list[Any]

    results: dict[str, Any]

    errors: list[str]
