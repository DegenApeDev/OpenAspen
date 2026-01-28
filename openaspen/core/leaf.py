from typing import Any, Callable, Optional, Dict, Awaitable
from openaspen.core.node import TreeNode
from pydantic import Field
import asyncio
import inspect


class Leaf(TreeNode):
    description: str = ""
    tool_func: Optional[Callable[..., Any]] = Field(default=None, exclude=True)
    is_async: bool = False
    parameters: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        name: str,
        tool_func: Optional[Callable[..., Any]] = None,
        description: str = "",
        llm_provider: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(name=name, llm_provider=llm_provider, description=description, **kwargs)
        self.tool_func = tool_func
        if tool_func:
            self.description = description or tool_func.__doc__ or ""
            self.is_async = asyncio.iscoroutinefunction(tool_func)
            self._extract_parameters()

    def _extract_parameters(self) -> None:
        if self.tool_func is None:
            return

        sig = inspect.signature(self.tool_func)
        self.parameters = {}
        for param_name, param in sig.parameters.items():
            param_info: Dict[str, Any] = {"name": param_name}
            if param.annotation != inspect.Parameter.empty:
                param_info["type"] = str(param.annotation)
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
            self.parameters[param_name] = param_info

    async def execute(self, input_data: Any, **kwargs: Any) -> Any:
        if self.tool_func is None:
            raise ValueError(f"Leaf '{self.name}' has no tool function defined")

        try:
            if self.is_async:
                result = await self.tool_func(input_data, **kwargs)
            else:
                result = await asyncio.to_thread(self.tool_func, input_data, **kwargs)

            return {
                "success": True,
                "result": result,
                "leaf": self.name,
                "path": "/".join(self.get_path()),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "leaf": self.name,
                "path": "/".join(self.get_path()),
            }

    def get_embedding_text(self) -> str:
        text_parts = [
            f"Skill: {self.name}",
            f"Description: {self.description}",
            f"Path: {'/'.join(self.get_path())}",
        ]
        if self.parameters:
            params_str = ", ".join(
                f"{name}: {info.get('type', 'Any')}" for name, info in self.parameters.items()
            )
            text_parts.append(f"Parameters: {params_str}")
        return "\n".join(text_parts)

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "description": self.description,
                "parameters": self.parameters,
                "is_async": self.is_async,
            }
        )
        return base_dict
