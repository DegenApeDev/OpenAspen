from typing import Dict, Any, Optional, List, Callable
from openaspen.core.branch import Branch
from openaspen.core.leaf import Leaf
from openaspen.llm.router import LLMRouter
from openaspen.llm.providers import LLMConfig
from openaspen.rag.store import GroupRAGStore
from openaspen.rag.embeddings import EmbeddingManager
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenAspenTree:
    def __init__(
        self,
        llm_configs: Dict[str, LLMConfig],
        shared_rag_db: Optional[GroupRAGStore] = None,
        embedding_manager: Optional[EmbeddingManager] = None,
        name: str = "OpenAspenTree",
        use_embeddings: bool = True,
    ):
        self.name = name
        self.llm_router = LLMRouter(llm_configs)
        
        # Only create embedding manager if requested and not provided
        if use_embeddings:
            self.embedding_manager = embedding_manager or EmbeddingManager(provider="fake")
            self.shared_rag_db = shared_rag_db or GroupRAGStore(
                embedding_manager=self.embedding_manager
            )
        else:
            self.embedding_manager = None
            self.shared_rag_db = None
            
        self.branches: List[Branch] = []
        self._execution_history: List[Dict[str, Any]] = []

    def add_branch(
        self,
        name: str,
        description: str = "",
        llm_provider: Optional[str] = None,
        system_prompt: str = "",
    ) -> Branch:
        branch = Branch(
            name=name,
            description=description,
            llm_provider=llm_provider,
            system_prompt=system_prompt,
        )
        self.branches.append(branch)
        logger.info(f"Added branch: {name}")
        return branch

    def grow_branch(self, name: str, **kwargs: Any) -> Branch:
        return self.add_branch(name, **kwargs)

    async def spawn_leaf(
        self,
        branch: Branch,
        skill_name: str,
        tool_func: Callable[..., Any],
        description: str = "",
        llm_provider: Optional[str] = None,
    ) -> Leaf:
        leaf = branch.add_leaf(skill_name, tool_func, description, llm_provider)
        await self.shared_rag_db.index_leaf(leaf, branch.name)
        logger.info(f"Spawned leaf: {skill_name} on branch: {branch.name}")
        return leaf

    async def index_tree(self) -> None:
        logger.info("Indexing entire tree in RAG database...")
        for branch in self.branches:
            await self.shared_rag_db.index_branch(branch)
        logger.info("Tree indexing complete")

    async def execute(self, query: str, **kwargs: Any) -> Dict[str, Any]:
        logger.info(f"Executing query: {query}")

        try:
            best_branch = await self._find_best_branch(query)

            if best_branch is None:
                return {
                    "success": False,
                    "error": "No suitable branch found",
                    "query": query,
                }

            result = await best_branch.execute(
                query,
                rag_db=self.shared_rag_db,
                llm_router=self.llm_router,
                **kwargs,
            )

            execution_record = {
                "query": query,
                "branch": best_branch.name,
                "result": result,
            }
            self._execution_history.append(execution_record)

            return result

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
            }

    async def _find_best_branch(self, query: str) -> Optional[Branch]:
        if not self.branches:
            return None

        if len(self.branches) == 1:
            return self.branches[0]

        try:
            results = await self.shared_rag_db.similarity_search_with_score(query, k=5)

            branch_scores: Dict[str, float] = {}
            for doc, score in results:
                branch_name = doc.metadata.get("branch")
                if branch_name:
                    branch_scores[branch_name] = branch_scores.get(branch_name, 0) + score

            if branch_scores:
                best_branch_name = max(branch_scores.items(), key=lambda x: x[1])[0]
                return next((b for b in self.branches if b.name == best_branch_name), None)

        except Exception as e:
            logger.warning(f"RAG-based branch selection failed: {e}")

        return self.branches[0]

    def get_branch(self, name: str) -> Optional[Branch]:
        return next((b for b in self.branches if b.name == name), None)

    def remove_branch(self, name: str) -> bool:
        branch = self.get_branch(name)
        if branch:
            self.branches.remove(branch)
            logger.info(f"Removed branch: {name}")
            return True
        return False

    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._execution_history[-limit:]

    def clear_history(self) -> None:
        self._execution_history.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "branches": [branch.to_dict() for branch in self.branches],
            "llm_providers": list(self.llm_router.get_available_providers()),
            "rag_stats": self.shared_rag_db.get_stats(),
        }

    def save_to_file(self, filepath: str) -> None:
        tree_data = self.to_dict()
        Path(filepath).write_text(json.dumps(tree_data, indent=2))
        logger.info(f"Saved tree to {filepath}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], llm_configs: Dict[str, LLMConfig]) -> "OpenAspenTree":
        tree = cls(llm_configs=llm_configs, name=data.get("name", "OpenAspenTree"))

        for branch_data in data.get("branches", []):
            branch = tree.add_branch(
                name=branch_data["name"],
                description=branch_data.get("description", ""),
                llm_provider=branch_data.get("llm_provider"),
                system_prompt=branch_data.get("system_prompt", ""),
            )

        return tree

    @classmethod
    def from_file(cls, filepath: str, llm_configs: Dict[str, LLMConfig]) -> "OpenAspenTree":
        data = json.loads(Path(filepath).read_text())
        return cls.from_dict(data, llm_configs)

    def visualize(self) -> str:
        lines = [f"🌲 {self.name}"]
        for i, branch in enumerate(self.branches):
            is_last_branch = i == len(self.branches) - 1
            branch_prefix = "└── " if is_last_branch else "├── "
            lines.append(f"{branch_prefix}🌿 {branch.name}")

            leaves = branch.get_leaves()
            for j, leaf in enumerate(leaves):
                is_last_leaf = j == len(leaves) - 1
                leaf_prefix = "    └── " if is_last_branch else "│   └── "
                if not is_last_leaf:
                    leaf_prefix = "    ├── " if is_last_branch else "│   ├── "
                lines.append(f"{leaf_prefix}🍃 {leaf.name}")

        return "\n".join(lines)

    async def __aenter__(self) -> "OpenAspenTree":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.shared_rag_db.persist()
