from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypedDict, Callable, Any
from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum
from ast import FunctionDef


class Rule(ABC):
    _registry: list[type[Rule]] = []
    name: str
    config: dict[str, Any]
    priority: int
    depend_on_ast: bool

    def __init_subclass__(cls, **kwargs) -> None:
        Rule._registry.append(cls)
        
        cls.name = cls.__name__
        cls.config = kwargs
        cls.priority = kwargs.pop("priority", 0)
        cls.depend_on_ast = kwargs.pop("depend_on_ast", False)

    @abstractmethod
    def __call__(self, route: RouteInfo) -> Issue | None:
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
    methods: Collection[str]

    # Optional Metadata
    status_code: int | None = None
    response_model: Any | None = None
    summary: str | None = None
    description: str | None = None
    tags: list[str | Enum] | None = None
    deprecated: bool | None = None
    strict_content_type: bool = True
    include_in_schema: bool = True

    # Optional ast - Route information
    body: dict[str, FunctionDef] | None = None # [Method: FunctionDef]

    @property
    def auto_generated_name(self) -> bool:
        return self.name == self.endpoint.__name__


class Issue(TypedDict):
    type: str
    level: str
    issue: str
    methods: list[str]
    categories: list[str]
    hint: str
    route_info: dict[Any, Any]