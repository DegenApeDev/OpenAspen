from typing import Any, Optional, List, Dict, Callable
from openaspen.core.node import TreeNode
from openaspen.core.leaf import Leaf
from pydantic import Field
import logging

logger = logging.getLogger(__name__)


class Branch(TreeNode):
    description: str = ""
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000

    def __init__(
        self,
        name: str,
        description: str = "",
        llm_provider: Optional[str] = None,
        system_prompt: str = "",
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            llm_provider=llm_provider,
            description=description,
            system_prompt=system_prompt,
            **kwargs,
        )

    def add_leaf(
        self,
        name: str,
        tool_func: Callable[..., Any],
        description: str = "",
        llm_provider: Optional[str] = None,
    ) -> Leaf:
        leaf = Leaf(
            name=name,
            tool_func=tool_func,
            description=description,
            llm_provider=llm_provider or self.llm_provider,
        )
        self.add_child(leaf)
        return leaf

    def get_leaves(self) -> List[Leaf]:
        return [child for child in self.children if isinstance(child, Leaf)]

    def get_branches(self) -> List["Branch"]:
        return [child for child in self.children if isinstance(child, Branch)]

    async def execute(self, input_data: Any, **kwargs: Any) -> Any:
        rag_db = kwargs.get("rag_db")
        llm_router = kwargs.get("llm_router")

        if rag_db and llm_router:
            relevant_leaves = await self._find_relevant_leaves(input_data, rag_db)
            if relevant_leaves:
                # Remove rag_db and llm_router from kwargs to avoid duplicate arguments
                filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ["rag_db", "llm_router"]}
                return await self._execute_with_llm(input_data, relevant_leaves, llm_router, **filtered_kwargs)

        if self.children:
            results = []
            for child in self.children:
                result = await child.execute(input_data, **kwargs)
                results.append(result)
            return {"success": True, "branch": self.name, "results": results}

        return {"success": False, "error": "No children to execute", "branch": self.name}

    async def _find_relevant_leaves(
        self, query: str, rag_db: Any, top_k: int = 3
    ) -> List[Leaf]:
        leaves = self.get_leaves()
        if not leaves:
            return []

        try:
            results = await rag_db.similarity_search(query, k=top_k, filter={"branch": self.name})
            relevant_leaf_names = [doc.metadata.get("leaf_name") for doc in results]
            return [leaf for leaf in leaves if leaf.name in relevant_leaf_names]
        except Exception as e:
            logger.warning(f"RAG search failed for branch {self.name}: {e}")
            return leaves[:top_k]

    async def _execute_with_llm(
        self,
        input_data: Any,
        relevant_leaves: List[Leaf],
        llm_router: Any,
        **kwargs: Any,
    ) -> Any:
        llm = await llm_router.get_llm(self.llm_provider or "openai")

        tools_description = "\n".join(
            [f"- {leaf.name}: {leaf.description}" for leaf in relevant_leaves]
        )

        prompt = f"""You are an AI agent in the {self.name} branch.
{self.system_prompt}

Available tools:
{tools_description}

User query: {input_data}

Select the most appropriate tool and provide the input for it.
Respond in JSON format: {{"tool": "tool_name", "input": "tool_input"}}
"""

        try:
            response = await llm.ainvoke(prompt)
            import json

            decision = json.loads(response.content if hasattr(response, "content") else str(response))

            selected_leaf = next(
                (leaf for leaf in relevant_leaves if leaf.name == decision.get("tool")), None
            )

            if selected_leaf:
                return await selected_leaf.execute(decision.get("input", input_data), **kwargs)
            else:
                return {
                    "success": False,
                    "error": f"Tool {decision.get('tool')} not found",
                    "branch": self.name,
                }
        except Exception as e:
            logger.error(f"LLM execution failed in branch {self.name}: {e}")
            if relevant_leaves:
                return await relevant_leaves[0].execute(input_data, **kwargs)
            return {"success": False, "error": str(e), "branch": self.name}

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "description": self.description,
                "system_prompt": self.system_prompt,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
        )
        return base_dict
