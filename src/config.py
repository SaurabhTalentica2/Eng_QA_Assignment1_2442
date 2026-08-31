"""Configuration and LLM setup for the QA Testing Duo.

Loads environment variables and builds a shared CrewAI LLM instance backed by
Google Gemini (free tier). Centralizing this keeps the agents free of
provider-specific wiring.
"""

import os

from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# LiteLLM-style model identifier. The "gemini/" prefix tells CrewAI/LiteLLM to
# use the Gemini API with a plain API key (no Vertex/GCP project needed).
MODEL_NAME = os.getenv("MODEL_NAME", "gemini/gemini-3.6-flash")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


def validate_config() -> None:
    """Fail fast with a clear message when the API key is not configured."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise ConfigError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your "
            "key from https://aistudio.google.com/app/apikey"
        )


def build_llm(temperature: float = 0.2) -> LLM:
    """Create the shared Gemini-backed LLM.

    A low temperature is used so requirement/test-case extraction stays
    deterministic and structured rather than creative.
    """
    validate_config()
    # LiteLLM reads the key from GEMINI_API_KEY in the environment; pass it
    # explicitly too so behavior is obvious and testable.
    return LLM(
        model=MODEL_NAME,
        api_key=GEMINI_API_KEY,
        temperature=temperature,
    )
