from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
import os


class EmbeddingManager:
    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
    ):
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._embeddings = self._create_embeddings()

    def _create_embeddings(self) -> Embeddings:
        if self.provider == "openai":
            return OpenAIEmbeddings(model=self.model, api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return await self._embeddings.aembed_documents(texts)

    async def embed_query(self, text: str) -> List[float]:
        return await self._embeddings.aembed_query(text)

    def get_embeddings(self) -> Embeddings:
        return self._embeddings
