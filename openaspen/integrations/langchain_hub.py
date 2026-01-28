from typing import Any, Callable, Dict, List, Optional, Union
from openaspen.core.leaf import Leaf
from openaspen.core.branch import Branch
import logging
import asyncio

logger = logging.getLogger(__name__)


class LangChainHubLoader:
    """
    Loader for LangChain Hub tools to integrate as OpenAspen leaves.
    Supports loading pre-built tools from langchain_community.tools.
    """

    AVAILABLE_TOOLS = {
        "tavily_search": {
            "import_path": "langchain_community.tools.tavily_search",
            "class_name": "TavilySearchResults",
            "description": "Search the web using Tavily API for real-time information",
            "default_params": {"max_results": 5},
            "requires_api_key": "TAVILY_API_KEY",
        },
        "duckduckgo_search": {
            "import_path": "langchain_community.tools",
            "class_name": "DuckDuckGoSearchRun",
            "description": "Search the web using DuckDuckGo (no API key required)",
            "default_params": {},
            "requires_api_key": None,
        },
        "wikipedia": {
            "import_path": "langchain_community.tools",
            "class_name": "WikipediaQueryRun",
            "description": "Search Wikipedia for encyclopedic information",
            "default_params": {},
            "requires_api_key": None,
        },
        "reddit_search": {
            "import_path": "langchain_community.tools.reddit_search.tool",
            "class_name": "RedditSearchRun",
            "description": "Search Reddit posts and comments",
            "default_params": {},
            "requires_api_key": None,
        },
        "youtube_search": {
            "import_path": "langchain_community.tools",
            "class_name": "YouTubeSearchTool",
            "description": "Search YouTube videos",
            "default_params": {},
            "requires_api_key": None,
        },
        "yahoo_finance_news": {
            "import_path": "langchain_community.tools.yahoo_finance_news",
            "class_name": "YahooFinanceNewsTool",
            "description": "Get financial news from Yahoo Finance",
            "default_params": {},
            "requires_api_key": None,
        },
        "requests_get": {
            "import_path": "langchain_community.tools",
            "class_name": "RequestsGetTool",
            "description": "Make HTTP GET requests to APIs",
            "default_params": {},
            "requires_api_key": None,
        },
        "requests_post": {
            "import_path": "langchain_community.tools",
            "class_name": "RequestsPostTool",
            "description": "Make HTTP POST requests to APIs",
            "default_params": {},
            "requires_api_key": None,
        },
        "python_repl": {
            "import_path": "langchain_experimental.tools",
            "class_name": "PythonREPLTool",
            "description": "Execute Python code in a REPL environment",
            "default_params": {},
            "requires_api_key": None,
        },
        "arxiv": {
            "import_path": "langchain_community.tools",
            "class_name": "ArxivQueryRun",
            "description": "Search arXiv for scientific papers",
            "default_params": {},
            "requires_api_key": None,
        },
    }

    @staticmethod
    def list_available_tools() -> List[str]:
        """List all available LangChain Hub tools."""
        return list(LangChainHubLoader.AVAILABLE_TOOLS.keys())

    @staticmethod
    def get_tool_info(tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool."""
        return LangChainHubLoader.AVAILABLE_TOOLS.get(tool_name)

    @staticmethod
    def load_tool(
        tool_name: str,
        custom_params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Load a LangChain tool by name.

        Args:
            tool_name: Name of the tool to load
            custom_params: Custom parameters to override defaults

        Returns:
            Instantiated LangChain tool

        Raises:
            ValueError: If tool is not found or cannot be loaded
        """
        tool_info = LangChainHubLoader.AVAILABLE_TOOLS.get(tool_name)
        if not tool_info:
            raise ValueError(
                f"Tool '{tool_name}' not found. Available tools: {LangChainHubLoader.list_available_tools()}"
            )

        try:
            import importlib

            module = importlib.import_module(tool_info["import_path"])
            tool_class = getattr(module, tool_info["class_name"])

            params = {**tool_info["default_params"]}
            if custom_params:
                params.update(custom_params)

            if tool_info["requires_api_key"]:
                import os

                api_key = os.getenv(tool_info["requires_api_key"])
                if not api_key:
                    logger.warning(
                        f"API key '{tool_info['requires_api_key']}' not found in environment. "
                        f"Tool '{tool_name}' may not work properly."
                    )

            tool_instance = tool_class(**params) if params else tool_class()
            logger.info(f"Loaded LangChain tool: {tool_name}")
            return tool_instance

        except ImportError as e:
            raise ValueError(
                f"Failed to import tool '{tool_name}'. "
                f"You may need to install additional dependencies: {e}"
            )
        except Exception as e:
            raise ValueError(f"Failed to load tool '{tool_name}': {e}")

    @staticmethod
    def create_leaf_from_hub(
        tool_name: str,
        leaf_name: Optional[str] = None,
        custom_params: Optional[Dict[str, Any]] = None,
        llm_provider: Optional[str] = None,
    ) -> Leaf:
        """
        Create an OpenAspen Leaf from a LangChain Hub tool.

        Args:
            tool_name: Name of the LangChain tool
            leaf_name: Custom name for the leaf (defaults to tool_name)
            custom_params: Custom parameters for the tool
            llm_provider: LLM provider for the leaf

        Returns:
            Leaf instance wrapping the LangChain tool
        """
        tool_info = LangChainHubLoader.AVAILABLE_TOOLS.get(tool_name)
        if not tool_info:
            raise ValueError(f"Tool '{tool_name}' not found")

        langchain_tool = LangChainHubLoader.load_tool(tool_name, custom_params)

        async def tool_wrapper(input_data: Any, **kwargs: Any) -> Any:
            """Wrapper to make LangChain tools compatible with OpenAspen Leaf interface."""
            try:
                if hasattr(langchain_tool, "arun"):
                    result = await langchain_tool.arun(input_data)
                elif hasattr(langchain_tool, "_arun"):
                    result = await langchain_tool._arun(input_data)
                elif hasattr(langchain_tool, "run"):
                    result = await asyncio.to_thread(langchain_tool.run, input_data)
                elif hasattr(langchain_tool, "_run"):
                    result = await asyncio.to_thread(langchain_tool._run, input_data)
                else:
                    result = await asyncio.to_thread(langchain_tool, input_data)
                return result
            except Exception as e:
                logger.error(f"Error executing LangChain tool '{tool_name}': {e}")
                raise

        leaf = Leaf(
            name=leaf_name or tool_name,
            tool_func=tool_wrapper,
            description=tool_info["description"],
            llm_provider=llm_provider,
        )

        leaf.metadata["langchain_tool"] = tool_name
        leaf.metadata["hub_source"] = "langchain_community"

        return leaf

    @staticmethod
    async def add_hub_tool_to_branch(
        branch: Branch,
        tool_name: str,
        leaf_name: Optional[str] = None,
        custom_params: Optional[Dict[str, Any]] = None,
        rag_db: Optional[Any] = None,
    ) -> Leaf:
        """
        Add a LangChain Hub tool as a leaf to a branch.

        Args:
            branch: Branch to add the leaf to
            tool_name: Name of the LangChain tool
            leaf_name: Custom name for the leaf
            custom_params: Custom parameters for the tool
            rag_db: Optional RAG database to index the leaf

        Returns:
            Created Leaf instance
        """
        leaf = LangChainHubLoader.create_leaf_from_hub(
            tool_name=tool_name,
            leaf_name=leaf_name,
            custom_params=custom_params,
            llm_provider=branch.llm_provider,
        )

        branch.add_child(leaf)

        if rag_db:
            await rag_db.index_leaf(leaf, branch.name)
            logger.info(f"Indexed leaf '{leaf.name}' in RAG database")

        logger.info(f"Added LangChain Hub tool '{tool_name}' as leaf '{leaf.name}' to branch '{branch.name}'")
        return leaf


def load_hub_tools(
    tool_names: Union[str, List[str]],
    llm: Optional[Any] = None,
) -> List[Any]:
    """
    Convenience function to load multiple LangChain tools at once.
    Compatible with LangChain's load_tools() pattern.

    Args:
        tool_names: Single tool name or list of tool names
        llm: Optional LLM instance (for compatibility, not used)

    Returns:
        List of loaded LangChain tools
    """
    if isinstance(tool_names, str):
        tool_names = [tool_names]

    tools = []
    for tool_name in tool_names:
        try:
            tool = LangChainHubLoader.load_tool(tool_name)
            tools.append(tool)
        except Exception as e:
            logger.error(f"Failed to load tool '{tool_name}': {e}")

    return tools
