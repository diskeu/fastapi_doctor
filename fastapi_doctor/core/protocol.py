from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypedDict, Callable, Any
from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum


class Rule(ABC):
    _registry: list[type[Rule]] = []
    name: str
    config: dict[str, Any]
    priority: int

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        Rule._registry.append(cls)
        
        cls.name = cls.__name__
        cls.config = kwargs
        cls.priority = kwargs.get("priority", 0)

    @abstractmethod
    def __call__(self, route: RouteInfo) -> dict[str, Any]:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...
    
    @abstractmethod
    def supports(self, route: RouteInfo) -> bool:
        ...

    @classmethod
    def iter_registry_sorted(cls):
        yield from sorted(
            Rule._registry,
            key=lambda rule: rule.priority
        )

    @classmethod
    def iter_registry(cls):
        yield from Rule._registry


@dataclass
class RouteInfo():
    path: str
    endpoint: Callable[..., Any]
    name: str

    # Optional Metadata
    methods: Collection[str] | None = None
    status_code: int | None = None
    response_model: Any | None = None
    summary: str | None = None
    description: str | None = None
    tags: list[str | Enum] | None = None
    deprecated: bool | None = None
    strict_content_type: bool = True
    include_in_schema: bool = True

    @property
    def auto_generated_name(self) -> bool:
        return self.name == self.endpoint.__name__


class Issue(TypedDict):
    type: str
    level: str
    issue: str
    method: str
    category: str
    hint: str
    route: RouteInfo