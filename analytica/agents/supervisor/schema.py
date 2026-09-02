from pydantic import BaseModel

from analytica.schema.agents_schema import SupervisorOutput


def get_schema() -> BaseModel:
    return SupervisorOutput
