from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field
import uuid


class TreeNode(ABC, BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    parent: Optional["TreeNode"] = Field(default=None, exclude=True)
    children: List["TreeNode"] = Field(default_factory=list, exclude=True)
    llm_provider: Optional[str] = None
    rag_context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    async def execute(self, input_data: Any, **kwargs: Any) -> Any:
        pass

    def add_child(self, child: "TreeNode") -> "TreeNode":
        child.parent = self
        self.children.append(child)
        return child

    def remove_child(self, child: "TreeNode") -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def get_path(self) -> List[str]:
        path = []
        current: Optional[TreeNode] = self
        while current is not None:
            path.insert(0, current.name)
            current = current.parent
        return path

    def get_depth(self) -> int:
        depth = 0
        current: Optional[TreeNode] = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth

    def find_child(self, name: str) -> Optional["TreeNode"]:
        for child in self.children:
            if child.name == name:
                return child
        return None

    def get_siblings(self) -> List["TreeNode"]:
        if self.parent is None:
            return []
        return [child for child in self.parent.children if child.id != self.id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "llm_provider": self.llm_provider,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children],
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', children={len(self.children)})"
