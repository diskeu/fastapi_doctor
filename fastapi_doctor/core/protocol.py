from __future__ import annotations
from fastapi_doctor.core.engine import RouteInfo
from abc import ABC, abstractmethod
from typing import Any


class Rule(ABC):
    _registry: list[type[Rule]] = []

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        Rule._registry.append(cls)
        
        cls.name = cls.__name__
        cls.config: dict[str, Any] = kwargs
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
