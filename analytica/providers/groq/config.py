"""
Configuration schema for Groq LLM model parameters.
"""

from pydantic.dataclasses import dataclass


@dataclass
class GroqModelConfig:
    """
    Data model defining configuration parameters for a Groq language model instance.

    Attributes:
        model: The identifier of the Groq model to use (e.g., 'llama-3.3-70b-versatile').
        temperature: Sampling temperature for output generation (0.0 to 2.0).
        max_retries: Maximum number of retries for failed API requests.
        max_tokens: Maximum number of tokens to generate in a response (optional).
    """

    model: str
    temperature: float
    max_retries: int
    reasoning_efforts: str | None = None
    max_tokens: int | None = None
