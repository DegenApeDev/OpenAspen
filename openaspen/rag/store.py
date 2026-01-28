from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from openaspen.rag.embeddings import EmbeddingManager
from openaspen.core.leaf import Leaf
from openaspen.core.branch import Branch
import logging

logger = logging.getLogger(__name__)


class GroupRAGStore:
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        embedding_manager: Optional[EmbeddingManager] = None,
    ):
        self.persist_directory = persist_directory
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self._vectorstore: Optional[Chroma] = None
        self._initialize_store()

    def _initialize_store(self) -> None:
        try:
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_manager.get_embeddings(),
            )
            logger.info(f"Initialized ChromaDB at {self.persist_directory}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise

    async def index_leaf(self, leaf: Leaf, branch_name: str) -> None:
        if self._vectorstore is None:
            raise ValueError("Vector store not initialized")

        text = leaf.get_embedding_text()
        metadata = {
            "leaf_name": leaf.name,
            "branch": branch_name,
            "type": "leaf",
            "description": leaf.description,
            "path": "/".join(leaf.get_path()),
        }

        doc = Document(page_content=text, metadata=metadata)
        await self._vectorstore.aadd_documents([doc])
        logger.debug(f"Indexed leaf: {leaf.name} in branch: {branch_name}")

    async def index_branch(self, branch: Branch) -> None:
        if self._vectorstore is None:
            raise ValueError("Vector store not initialized")

        for leaf in branch.get_leaves():
            await self.index_leaf(leaf, branch.name)

        for sub_branch in branch.get_branches():
            await self.index_branch(sub_branch)

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        if self._vectorstore is None:
            raise ValueError("Vector store not initialized")

        try:
            results = await self._vectorstore.asimilarity_search(query, k=k, filter=filter)
            return results
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    async def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[tuple[Document, float]]:
        if self._vectorstore is None:
            raise ValueError("Vector store not initialized")

        try:
            results = await self._vectorstore.asimilarity_search_with_score(
                query, k=k, filter=filter
            )
            return results
        except Exception as e:
            logger.error(f"Similarity search with score failed: {e}")
            return []

    async def get_sibling_context(self, branch_name: str, query: str, k: int = 3) -> List[Document]:
        results = await self.similarity_search(query, k=k * 2)
        sibling_docs = [doc for doc in results if doc.metadata.get("branch") != branch_name]
        return sibling_docs[:k]

    def clear(self) -> None:
        if self._vectorstore is not None:
            self._vectorstore.delete_collection()
            self._initialize_store()
            logger.info("Cleared vector store")

    def persist(self) -> None:
        if self._vectorstore is not None:
            self._vectorstore.persist()
            logger.info("Persisted vector store")

    def get_stats(self) -> Dict[str, Any]:
        if self._vectorstore is None:
            return {"error": "Vector store not initialized"}

        try:
            collection = self._vectorstore._collection
            count = collection.count()
            return {
                "total_documents": count,
                "persist_directory": self.persist_directory,
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}
