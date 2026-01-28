import pytest
from unittest.mock import Mock, AsyncMock, patch
from openaspen.integrations.langchain_hub import LangChainHubLoader, load_hub_tools
from openaspen.core.branch import Branch
from openaspen.core.leaf import Leaf


class TestLangChainHubLoader:
    def test_list_available_tools(self):
        tools = LangChainHubLoader.list_available_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
        assert "duckduckgo_search" in tools
        assert "wikipedia" in tools
        assert "tavily_search" in tools

    def test_get_tool_info(self):
        info = LangChainHubLoader.get_tool_info("duckduckgo_search")
        assert info is not None
        assert "description" in info
        assert "import_path" in info
        assert "class_name" in info
        assert info["class_name"] == "DuckDuckGoSearchRun"

    def test_get_tool_info_invalid(self):
        info = LangChainHubLoader.get_tool_info("nonexistent_tool")
        assert info is None

    @patch("openaspen.integrations.langchain_hub.importlib.import_module")
    def test_load_tool_success(self, mock_import):
        mock_tool_class = Mock()
        mock_tool_instance = Mock()
        mock_tool_class.return_value = mock_tool_instance

        mock_module = Mock()
        mock_module.DuckDuckGoSearchRun = mock_tool_class
        mock_import.return_value = mock_module

        tool = LangChainHubLoader.load_tool("duckduckgo_search")

        assert tool == mock_tool_instance
        mock_import.assert_called_once()
        mock_tool_class.assert_called_once()

    def test_load_tool_invalid_name(self):
        with pytest.raises(ValueError, match="Tool 'invalid_tool' not found"):
            LangChainHubLoader.load_tool("invalid_tool")

    @patch("openaspen.integrations.langchain_hub.importlib.import_module")
    def test_load_tool_with_custom_params(self, mock_import):
        mock_tool_class = Mock()
        mock_tool_instance = Mock()
        mock_tool_class.return_value = mock_tool_instance

        mock_module = Mock()
        mock_module.TavilySearchResults = mock_tool_class
        mock_import.return_value = mock_module

        custom_params = {"max_results": 10}
        tool = LangChainHubLoader.load_tool("tavily_search", custom_params)

        assert tool == mock_tool_instance
        mock_tool_class.assert_called_once_with(max_results=10)

    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    def test_create_leaf_from_hub(self, mock_load_tool):
        mock_tool = Mock()
        mock_tool.run = Mock(return_value="test result")
        mock_load_tool.return_value = mock_tool

        leaf = LangChainHubLoader.create_leaf_from_hub(
            tool_name="duckduckgo_search",
            leaf_name="test_search",
            llm_provider="openai",
        )

        assert isinstance(leaf, Leaf)
        assert leaf.name == "test_search"
        assert leaf.description == "Search the web using DuckDuckGo (no API key required)"
        assert leaf.llm_provider == "openai"
        assert leaf.metadata["langchain_tool"] == "duckduckgo_search"
        assert leaf.metadata["hub_source"] == "langchain_community"
        mock_load_tool.assert_called_once_with("duckduckgo_search", None)

    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    def test_create_leaf_from_hub_default_name(self, mock_load_tool):
        mock_tool = Mock()
        mock_load_tool.return_value = mock_tool

        leaf = LangChainHubLoader.create_leaf_from_hub(tool_name="wikipedia")

        assert leaf.name == "wikipedia"

    @pytest.mark.asyncio
    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.create_leaf_from_hub")
    async def test_add_hub_tool_to_branch(self, mock_create_leaf):
        mock_leaf = Mock(spec=Leaf)
        mock_leaf.name = "test_leaf"
        mock_create_leaf.return_value = mock_leaf

        branch = Branch(name="test_branch", llm_provider="openai")
        mock_rag_db = AsyncMock()

        leaf = await LangChainHubLoader.add_hub_tool_to_branch(
            branch=branch,
            tool_name="duckduckgo_search",
            leaf_name="search",
            rag_db=mock_rag_db,
        )

        assert leaf == mock_leaf
        assert len(branch.children) == 1
        assert branch.children[0] == mock_leaf
        mock_rag_db.index_leaf.assert_called_once_with(mock_leaf, "test_branch")

    @pytest.mark.asyncio
    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.create_leaf_from_hub")
    async def test_add_hub_tool_to_branch_no_rag(self, mock_create_leaf):
        mock_leaf = Mock(spec=Leaf)
        mock_leaf.name = "test_leaf"
        mock_create_leaf.return_value = mock_leaf

        branch = Branch(name="test_branch", llm_provider="openai")

        leaf = await LangChainHubLoader.add_hub_tool_to_branch(
            branch=branch, tool_name="wikipedia", leaf_name="wiki"
        )

        assert leaf == mock_leaf
        assert len(branch.children) == 1

    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    def test_load_hub_tools_single(self, mock_load_tool):
        mock_tool = Mock()
        mock_load_tool.return_value = mock_tool

        tools = load_hub_tools("duckduckgo_search")

        assert len(tools) == 1
        assert tools[0] == mock_tool
        mock_load_tool.assert_called_once_with("duckduckgo_search")

    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    def test_load_hub_tools_multiple(self, mock_load_tool):
        mock_tool1 = Mock()
        mock_tool2 = Mock()
        mock_load_tool.side_effect = [mock_tool1, mock_tool2]

        tools = load_hub_tools(["duckduckgo_search", "wikipedia"])

        assert len(tools) == 2
        assert tools[0] == mock_tool1
        assert tools[1] == mock_tool2
        assert mock_load_tool.call_count == 2

    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    def test_load_hub_tools_with_failures(self, mock_load_tool):
        mock_tool = Mock()
        mock_load_tool.side_effect = [mock_tool, ValueError("Tool not found")]

        tools = load_hub_tools(["duckduckgo_search", "invalid_tool"])

        assert len(tools) == 1
        assert tools[0] == mock_tool

    @pytest.mark.asyncio
    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    async def test_leaf_execution_with_arun(self, mock_load_tool):
        mock_tool = AsyncMock()
        mock_tool.arun = AsyncMock(return_value="async result")
        mock_load_tool.return_value = mock_tool

        leaf = LangChainHubLoader.create_leaf_from_hub(tool_name="duckduckgo_search")

        result = await leaf.execute("test query")

        assert result["success"] is True
        assert result["result"] == "async result"
        assert result["leaf"] == "duckduckgo_search"
        mock_tool.arun.assert_called_once_with("test query")

    @pytest.mark.asyncio
    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    async def test_leaf_execution_with_run(self, mock_load_tool):
        mock_tool = Mock()
        mock_tool.run = Mock(return_value="sync result")
        delattr(mock_tool, "arun")
        delattr(mock_tool, "_arun")
        mock_load_tool.return_value = mock_tool

        leaf = LangChainHubLoader.create_leaf_from_hub(tool_name="duckduckgo_search")

        result = await leaf.execute("test query")

        assert result["success"] is True
        assert result["result"] == "sync result"
        assert result["leaf"] == "duckduckgo_search"

    @pytest.mark.asyncio
    @patch("openaspen.integrations.langchain_hub.LangChainHubLoader.load_tool")
    async def test_leaf_execution_error_handling(self, mock_load_tool):
        mock_tool = Mock()
        mock_tool.run = Mock(side_effect=Exception("Tool error"))
        delattr(mock_tool, "arun")
        delattr(mock_tool, "_arun")
        mock_load_tool.return_value = mock_tool

        leaf = LangChainHubLoader.create_leaf_from_hub(tool_name="duckduckgo_search")

        result = await leaf.execute("test query")

        assert result["success"] is False
        assert "Tool error" in result["error"]
        assert result["leaf"] == "duckduckgo_search"


class TestToolMetadata:
    def test_all_tools_have_required_fields(self):
        required_fields = ["import_path", "class_name", "description", "default_params", "requires_api_key"]

        for tool_name, tool_info in LangChainHubLoader.AVAILABLE_TOOLS.items():
            for field in required_fields:
                assert field in tool_info, f"Tool '{tool_name}' missing field '{field}'"

    def test_tool_descriptions_not_empty(self):
        for tool_name, tool_info in LangChainHubLoader.AVAILABLE_TOOLS.items():
            assert tool_info["description"], f"Tool '{tool_name}' has empty description"
            assert len(tool_info["description"]) > 10, f"Tool '{tool_name}' description too short"
