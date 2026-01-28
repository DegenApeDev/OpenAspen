from typing import List, Optional
from langchain.embeddings.base import Embeddings
import os


class EmbeddingManager:
    def __init__(
        self,
        provider: str = "huggingface",
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
        api_key: Optional[str] = None,
    ):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self._embeddings = self._create_embeddings()

    def _create_embeddings(self) -> Embeddings:
        if self.provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key required for OpenAI embeddings. Set OPENAI_API_KEY or use provider='huggingface'")
            return OpenAIEmbeddings(model=self.model, api_key=api_key)
        elif self.provider == "huggingface":
            try:
                from langchain_huggingface import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(model_name=self.model)
            except ImportError:
                # Fallback to fake embeddings if HuggingFace not installed
                try:
                    from langchain_community.embeddings import FakeEmbeddings
                    return FakeEmbeddings(size=384)
                except ImportError:
                    from langchain_core.embeddings.fake import FakeEmbeddings
                    return FakeEmbeddings(size=384)
        elif self.provider == "fake":
            try:
                from langchain_community.embeddings import FakeEmbeddings
                return FakeEmbeddings(size=384)
            except ImportError:
                from langchain_core.embeddings.fake import FakeEmbeddings
                return FakeEmbeddings(size=384)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}. Use 'huggingface', 'openai', or 'fake'")

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return await self._embeddings.aembed_documents(texts)

    async def embed_query(self, text: str) -> List[float]:
        return await self._embeddings.aembed_query(text)

    def get_embeddings(self) -> Embeddings:
        return self._embeddings
