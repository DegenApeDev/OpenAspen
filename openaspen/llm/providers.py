from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROK = "grok"
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"


class LLMConfig(BaseModel):
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    cost_per_1k_tokens: float = 0.0
    speed_score: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


PROVIDER_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "openai": {
        "model": "gpt-4-turbo-preview",
        "cost_per_1k_tokens": 0.01,
        "speed_score": 0.8,
    },
    "anthropic": {
        "model": "claude-3-opus-20240229",
        "cost_per_1k_tokens": 0.015,
        "speed_score": 0.7,
    },
    "grok": {
        "model": "grok-1",
        "api_base": "https://api.x.ai/v1",
        "cost_per_1k_tokens": 0.005,
        "speed_score": 0.9,
    },
    "ollama": {
        "model": "llama2",
        "api_base": "http://localhost:11434",
        "cost_per_1k_tokens": 0.0,
        "speed_score": 0.6,
    },
    "lmstudio": {
        "model": "local-model",
        "api_base": "http://localhost:1234/v1",
        "cost_per_1k_tokens": 0.0,
        "speed_score": 0.5,
    },
}


def create_llm_config(
    provider: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs: Any,
) -> LLMConfig:
    defaults = PROVIDER_DEFAULTS.get(provider, {})
    
    # For local providers, set a dummy API key if not provided
    if provider in ["ollama", "lmstudio"] and api_key is None:
        api_key = "not-needed"
    
    config_data = {
        "provider": provider,
        "model": model or defaults.get("model", "default"),
        "api_key": api_key,
        **defaults,
        **kwargs,
    }
    return LLMConfig(**config_data)
