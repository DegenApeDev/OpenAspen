from typing import Dict, Optional, Any, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chat_models.base import BaseChatModel
from openaspen.llm.providers import LLMConfig, LLMProvider
import logging
import os

logger = logging.getLogger(__name__)


class LLMRouter:
    def __init__(self, configs: Dict[str, LLMConfig]):
        self.configs = configs
        self._llm_cache: Dict[str, BaseChatModel] = {}
        self._initialize_llms()

    def _initialize_llms(self) -> None:
        for provider_name, config in self.configs.items():
            try:
                llm = self._create_llm(config)
                self._llm_cache[provider_name] = llm
                logger.info(f"Initialized LLM provider: {provider_name}")
            except Exception as e:
                logger.error(f"Failed to initialize {provider_name}: {e}")

    def _create_llm(self, config: LLMConfig) -> BaseChatModel:
        # For local providers, use dummy API key if not provided
        if config.provider in [LLMProvider.OLLAMA, LLMProvider.LMSTUDIO]:
            api_key = config.api_key or "not-needed"
        else:
            api_key = config.api_key or os.getenv(f"{config.provider.upper()}_API_KEY")

        if config.provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model=config.model,
                api_key=api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
            )
        elif config.provider == LLMProvider.ANTHROPIC:
            return ChatAnthropic(
                model=config.model,
                api_key=api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
            )
        elif config.provider == LLMProvider.GROK:
            return ChatOpenAI(
                model=config.model,
                api_key=api_key,
                base_url=config.api_base,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
            )
        elif config.provider in [LLMProvider.OLLAMA, LLMProvider.LMSTUDIO]:
            return ChatOpenAI(
                model=config.model,
                base_url=config.api_base,
                api_key="not-needed",
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout,
            )
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

    async def get_llm(self, provider_name: Optional[str] = None) -> BaseChatModel:
        if provider_name and provider_name in self._llm_cache:
            return self._llm_cache[provider_name]

        if not self._llm_cache:
            raise ValueError("No LLM providers configured")

        return list(self._llm_cache.values())[0]

    def route_by_cost(self, max_cost_per_1k: float = 0.01) -> Optional[str]:
        eligible = [
            (name, config)
            for name, config in self.configs.items()
            if config.cost_per_1k_tokens <= max_cost_per_1k
        ]
        if not eligible:
            return None
        return max(eligible, key=lambda x: x[1].speed_score)[0]

    def route_by_speed(self, min_speed_score: float = 0.5) -> Optional[str]:
        eligible = [
            (name, config)
            for name, config in self.configs.items()
            if config.speed_score >= min_speed_score
        ]
        if not eligible:
            return None
        return max(eligible, key=lambda x: x[1].speed_score)[0]

    def route_by_skill(self, skill_type: str) -> Optional[str]:
        skill_mapping = {
            "coding": ["openai", "anthropic"],
            "creative": ["anthropic", "grok"],
            "fast": ["grok", "ollama"],
            "local": ["ollama", "lmstudio"],
        }

        preferred_providers = skill_mapping.get(skill_type, [])
        for provider in preferred_providers:
            if provider in self._llm_cache:
                return provider

        return list(self._llm_cache.keys())[0] if self._llm_cache else None

    def get_available_providers(self) -> List[str]:
        return list(self._llm_cache.keys())

    def add_provider(self, name: str, config: LLMConfig) -> None:
        self.configs[name] = config
        try:
            llm = self._create_llm(config)
            self._llm_cache[name] = llm
            logger.info(f"Added LLM provider: {name}")
        except Exception as e:
            logger.error(f"Failed to add provider {name}: {e}")

    def remove_provider(self, name: str) -> None:
        if name in self.configs:
            del self.configs[name]
        if name in self._llm_cache:
            del self._llm_cache[name]
            logger.info(f"Removed LLM provider: {name}")
