import pytest
from openaspen.llm.providers import LLMProvider, LLMConfig, create_llm_config, PROVIDER_DEFAULTS
from openaspen.llm.router import LLMRouter


class TestLLMProviders:
    def test_llm_provider_enum(self) -> None:
        assert LLMProvider.OPENAI == "openai"
        assert LLMProvider.ANTHROPIC == "anthropic"
        assert LLMProvider.GROK == "grok"
        assert LLMProvider.OLLAMA == "ollama"

    def test_create_llm_config(self) -> None:
        config = create_llm_config(
            provider="openai",
            model="gpt-4",
            api_key="test-key",
        )
        assert config.provider == LLMProvider.OPENAI
        assert config.model == "gpt-4"
        assert config.api_key == "test-key"

    def test_create_llm_config_with_defaults(self) -> None:
        config = create_llm_config(provider="openai")
        assert config.model == PROVIDER_DEFAULTS["openai"]["model"]
        assert config.cost_per_1k_tokens == PROVIDER_DEFAULTS["openai"]["cost_per_1k_tokens"]

    def test_llm_config_validation(self) -> None:
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            temperature=0.5,
            max_tokens=1000,
        )
        assert config.temperature == 0.5
        assert config.max_tokens == 1000


class TestLLMRouter:
    def test_router_initialization(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        router = LLMRouter(configs)
        assert "openai" in router.get_available_providers()

    def test_route_by_cost(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai"),
            "ollama": create_llm_config(provider="ollama"),
        }
        router = LLMRouter(configs)

        cheap_provider = router.route_by_cost(max_cost_per_1k=0.001)
        assert cheap_provider == "ollama"

    def test_route_by_speed(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai"),
            "grok": create_llm_config(provider="grok"),
        }
        router = LLMRouter(configs)

        fast_provider = router.route_by_speed(min_speed_score=0.8)
        assert fast_provider in ["openai", "grok"]

    def test_route_by_skill(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai"),
            "anthropic": create_llm_config(provider="anthropic"),
        }
        router = LLMRouter(configs)

        coding_provider = router.route_by_skill("coding")
        assert coding_provider in ["openai", "anthropic"]

    def test_add_provider(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai"),
        }
        router = LLMRouter(configs)

        new_config = create_llm_config(provider="ollama")
        router.add_provider("ollama", new_config)

        assert "ollama" in router.get_available_providers()

    def test_remove_provider(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai"),
            "ollama": create_llm_config(provider="ollama"),
        }
        router = LLMRouter(configs)

        router.remove_provider("ollama")
        assert "ollama" not in router.get_available_providers()
