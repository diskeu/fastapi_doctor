from fastapi_doctor.core.protocol import Rule
from typing import Any, Callable

def rule(*, config: dict[str, Any] | None = None, priority: int = 0) -> Callable[[type[Any]], type[Rule]]:
    if not config: config = {}

    def inner(cls) -> type[Rule]:
        # Due classes also don't get checked on the correct implementation
        # of abstract methods, it'd be better to not check them directly
        # when creating them with the `type` function.
        name: str = cls.__name__
        bases: tuple[type[Any], ...] = (Rule, )
        methods: dict[str, Any] = {
            "__call__": cls.call,
            "description": cls.description,
            "supports": cls.supports
        }
        rule: type[Rule] = type(name, bases, methods)

        rule.config = cls.config | config
        rule.priority = priority
        return rule
    return inner