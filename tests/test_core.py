import pytest
from openaspen.core.node import TreeNode
from openaspen.core.branch import Branch
from openaspen.core.leaf import Leaf


async def sample_tool(input_data: str) -> str:
    return f"Processed: {input_data}"


def sync_tool(input_data: str) -> str:
    return f"Sync processed: {input_data}"


class TestTreeNode:
    def test_node_creation(self) -> None:
        branch = Branch(name="test_branch")
        assert branch.name == "test_branch"
        assert len(branch.children) == 0
        assert branch.parent is None

    def test_add_child(self) -> None:
        parent = Branch(name="parent")
        child = Branch(name="child")
        parent.add_child(child)

        assert len(parent.children) == 1
        assert child.parent == parent

    def test_get_path(self) -> None:
        root = Branch(name="root")
        child = Branch(name="child")
        grandchild = Branch(name="grandchild")

        root.add_child(child)
        child.add_child(grandchild)

        assert grandchild.get_path() == ["root", "child", "grandchild"]

    def test_get_depth(self) -> None:
        root = Branch(name="root")
        child = Branch(name="child")
        grandchild = Branch(name="grandchild")

        root.add_child(child)
        child.add_child(grandchild)

        assert root.get_depth() == 0
        assert child.get_depth() == 1
        assert grandchild.get_depth() == 2

    def test_find_child(self) -> None:
        parent = Branch(name="parent")
        child1 = Branch(name="child1")
        child2 = Branch(name="child2")

        parent.add_child(child1)
        parent.add_child(child2)

        found = parent.find_child("child2")
        assert found is not None
        assert found.name == "child2"

    def test_get_siblings(self) -> None:
        parent = Branch(name="parent")
        child1 = Branch(name="child1")
        child2 = Branch(name="child2")
        child3 = Branch(name="child3")

        parent.add_child(child1)
        parent.add_child(child2)
        parent.add_child(child3)

        siblings = child2.get_siblings()
        assert len(siblings) == 2
        assert child1 in siblings
        assert child3 in siblings


class TestLeaf:
    @pytest.mark.asyncio
    async def test_leaf_creation(self) -> None:
        leaf = Leaf(name="test_leaf", tool_func=sample_tool, description="Test tool")
        assert leaf.name == "test_leaf"
        assert leaf.description == "Test tool"
        assert leaf.is_async is True

    @pytest.mark.asyncio
    async def test_leaf_execute_async(self) -> None:
        leaf = Leaf(name="test_leaf", tool_func=sample_tool)
        result = await leaf.execute("test input")

        assert result["success"] is True
        assert "Processed: test input" in result["result"]
        assert result["leaf"] == "test_leaf"

    @pytest.mark.asyncio
    async def test_leaf_execute_sync(self) -> None:
        leaf = Leaf(name="sync_leaf", tool_func=sync_tool)
        result = await leaf.execute("test input")

        assert result["success"] is True
        assert "Sync processed: test input" in result["result"]

    def test_leaf_embedding_text(self) -> None:
        leaf = Leaf(name="test_leaf", tool_func=sample_tool, description="A test tool")
        embedding_text = leaf.get_embedding_text()

        assert "test_leaf" in embedding_text
        assert "A test tool" in embedding_text


class TestBranch:
    def test_branch_creation(self) -> None:
        branch = Branch(
            name="test_branch",
            description="Test branch",
            llm_provider="openai",
        )
        assert branch.name == "test_branch"
        assert branch.description == "Test branch"
        assert branch.llm_provider == "openai"

    def test_add_leaf(self) -> None:
        branch = Branch(name="test_branch")
        leaf = branch.add_leaf("test_leaf", sample_tool, "Test description")

        assert len(branch.children) == 1
        assert isinstance(leaf, Leaf)
        assert leaf.name == "test_leaf"

    def test_get_leaves(self) -> None:
        branch = Branch(name="test_branch")
        leaf1 = branch.add_leaf("leaf1", sample_tool)
        leaf2 = branch.add_leaf("leaf2", sample_tool)

        leaves = branch.get_leaves()
        assert len(leaves) == 2
        assert leaf1 in leaves
        assert leaf2 in leaves

    def test_get_branches(self) -> None:
        parent = Branch(name="parent")
        child_branch = Branch(name="child_branch")
        parent.add_child(child_branch)
        parent.add_leaf("leaf", sample_tool)

        branches = parent.get_branches()
        assert len(branches) == 1
        assert child_branch in branches
