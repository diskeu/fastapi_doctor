from fastapi_doctor.core.protocol import Rule
from typing import Any, Callable


def rule(*, config: dict[str, Any] | None = None, priority: int | None = None, depend_on_ast: bool = False) -> Callable[[type[Any]], type[Rule]]:
    def inner(cls) -> type[Rule]:
        name: str = cls.__name__

        bases: tuple[type[Any], ...] = (Rule, )

        methods: dict[str, Any] = {
            method_name: getattr(cls, method_name)
            for method_name in [
                "__call__",
                "description",
                "supports"
            ]
            if hasattr(cls, method_name)
        }

        rule: type[Rule] = type(name, bases, methods)
        if config: rule.config = config
        if priority is not None: rule.priority = priority
        if depend_on_ast: rule.depend_on_ast = depend_on_ast

        return rule
    return inner