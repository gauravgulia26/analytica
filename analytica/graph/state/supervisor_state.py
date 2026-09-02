from enum import Enum
from typing import Any, TypedDict


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(TypedDict):
    id: str
    task: str
    status: TaskStatus
    agent: str | None
    result: Any
    depends_on: list[str]


class SupervisorState(TypedDict):
    user_request: str

    tasks: list[Task]

    current_task: str | None
    current_agent: str | None

    results: dict[str, Any]

    errors: list[str]
