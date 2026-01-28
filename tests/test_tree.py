import pytest
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config


async def test_tool(input_data: str) -> str:
    return f"Result: {input_data}"


class TestOpenAspenTree:
    def test_tree_creation(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs, name="TestTree")
        assert tree.name == "TestTree"
        assert len(tree.branches) == 0

    def test_add_branch(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)
        branch = tree.add_branch("test_branch", description="Test")

        assert len(tree.branches) == 1
        assert branch.name == "test_branch"

    def test_grow_branch(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)
        branch = tree.grow_branch("test_branch")

        assert len(tree.branches) == 1
        assert branch.name == "test_branch"

    @pytest.mark.asyncio
    async def test_spawn_leaf(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)
        branch = tree.add_branch("test_branch")

        leaf = await tree.spawn_leaf(branch, "test_leaf", test_tool, "Test tool")

        assert leaf.name == "test_leaf"
        assert len(branch.children) == 1

    def test_get_branch(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)
        tree.add_branch("branch1")
        tree.add_branch("branch2")

        found = tree.get_branch("branch2")
        assert found is not None
        assert found.name == "branch2"

    def test_remove_branch(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)
        tree.add_branch("branch1")
        tree.add_branch("branch2")

        removed = tree.remove_branch("branch1")
        assert removed is True
        assert len(tree.branches) == 1
        assert tree.get_branch("branch1") is None

    def test_visualize(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs, name="TestTree")
        branch = tree.add_branch("test_branch")

        viz = tree.visualize()
        assert "TestTree" in viz
        assert "test_branch" in viz

    def test_to_dict(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs, name="TestTree")
        tree.add_branch("branch1", description="First branch")

        tree_dict = tree.to_dict()
        assert tree_dict["name"] == "TestTree"
        assert len(tree_dict["branches"]) == 1
        assert tree_dict["branches"][0]["name"] == "branch1"

    def test_execution_history(self) -> None:
        configs = {
            "openai": create_llm_config(provider="openai", api_key="test"),
        }
        tree = OpenAspenTree(llm_configs=configs)

        tree._execution_history.append({"query": "test1", "result": "result1"})
        tree._execution_history.append({"query": "test2", "result": "result2"})

        history = tree.get_execution_history(limit=5)
        assert len(history) == 2

        tree.clear_history()
        assert len(tree.get_execution_history()) == 0
