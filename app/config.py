import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LiteLLM Configuration
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "openai/gpt-4o")

def get_model_config() -> dict:
    """Get model configuration for LiteLLM."""
    return {"model": DEFAULT_LLM_MODEL}