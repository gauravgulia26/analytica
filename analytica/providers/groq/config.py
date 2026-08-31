from pydantic.dataclasses import dataclass


@dataclass
class GroqModelConfig:
    model: str
    temperature: float
    max_retries: int
    max_tokens: int | None = None
