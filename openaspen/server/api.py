from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from openaspen import OpenAspenTree
from openaspen.llm.providers import create_llm_config
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "openaspen"
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 2000
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    id: str = "chatcmpl-openaspen"
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(__import__("time").time()))
    model: str = "openaspen"
    choices: List[Dict[str, Any]]
    usage: Dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


class TreeInfo(BaseModel):
    name: str
    branches: List[str]
    llm_providers: List[str]


def create_app(config_file: Optional[str] = None) -> FastAPI:
    app = FastAPI(
        title="OpenAspen API",
        description="OpenAI-compatible API for OpenAspen tree-structured agents",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    tree: Optional[OpenAspenTree] = None

    if config_file and Path(config_file).exists():
        config_data = json.loads(Path(config_file).read_text())
        llm_configs = {}
        for name, config in config_data.get("llm_providers", {}).items():
            llm_configs[name] = create_llm_config(**config)
        tree = OpenAspenTree.from_dict(config_data, llm_configs)
        logger.info(f"Loaded tree from {config_file}")

    @app.get("/")
    async def root() -> Dict[str, str]:
        return {
            "name": "OpenAspen API",
            "version": "0.1.0",
            "status": "running",
        }

    @app.get("/v1/models")
    async def list_models() -> Dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {
                    "id": "openaspen",
                    "object": "model",
                    "created": 1234567890,
                    "owned_by": "openaspen",
                }
            ],
        }

    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
        if tree is None:
            raise HTTPException(status_code=500, detail="Tree not initialized")

        try:
            last_message = request.messages[-1].content if request.messages else ""

            result = await tree.execute(last_message)

            response_content = json.dumps(result) if isinstance(result, dict) else str(result)

            return ChatCompletionResponse(
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": response_content},
                        "finish_reason": "stop",
                    }
                ],
            )
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/tree/info")
    async def get_tree_info() -> TreeInfo:
        if tree is None:
            raise HTTPException(status_code=500, detail="Tree not initialized")

        return TreeInfo(
            name=tree.name,
            branches=[b.name for b in tree.branches],
            llm_providers=tree.llm_router.get_available_providers(),
        )

    @app.get("/tree/visualize")
    async def visualize_tree() -> Dict[str, str]:
        if tree is None:
            raise HTTPException(status_code=500, detail="Tree not initialized")

        return {"visualization": tree.visualize()}

    @app.post("/tree/execute")
    async def execute_query(query: str) -> Dict[str, Any]:
        if tree is None:
            raise HTTPException(status_code=500, detail="Tree not initialized")

        result = await tree.execute(query)
        return result

    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        return {"status": "healthy"}

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)
