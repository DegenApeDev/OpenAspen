import pytest
from openaspen.rag.embeddings import EmbeddingManager
from openaspen.core.leaf import Leaf
from openaspen.core.branch import Branch


async def dummy_tool(input_data: str) -> str:
    return "result"


class TestEmbeddingManager:
    def test_embedding_manager_creation(self) -> None:
        manager = EmbeddingManager(provider="openai", api_key="test")
        assert manager.provider == "openai"
        assert manager.api_key == "test"

    def test_get_embeddings(self) -> None:
        manager = EmbeddingManager(provider="openai", api_key="test")
        embeddings = manager.get_embeddings()
        assert embeddings is not None


class TestLeafEmbedding:
    def test_leaf_embedding_text(self) -> None:
        leaf = Leaf(
            name="test_leaf",
            tool_func=dummy_tool,
            description="A test leaf for embedding",
        )

        embedding_text = leaf.get_embedding_text()
        assert "test_leaf" in embedding_text
        assert "A test leaf for embedding" in embedding_text

    def test_leaf_with_parameters(self) -> None:
        def tool_with_params(name: str, age: int = 25) -> str:
            return f"{name} is {age}"

        leaf = Leaf(
            name="param_leaf",
            tool_func=tool_with_params,
            description="Tool with parameters",
        )

        embedding_text = leaf.get_embedding_text()
        assert "param_leaf" in embedding_text
        assert "Parameters:" in embedding_text
