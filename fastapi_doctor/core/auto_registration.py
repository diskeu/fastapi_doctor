from fastapi_doctor.core.protocol import Rule
from typing import Any

def rule(*, config: dict[str, Any], priority: int = 0):
    def inner(cls):
        # Due classes also don't get checked on the correct implementation
        # of abstract methods, it'd be better to not check them directly
        # when creating them with the `type` function.
        # for method in ("__check__", "description", "supports"):
        #     if not hasattr(cls, method):
        #         raise TypeError(f"{cls} does not support `{method}`.")
        rule = type(
            name="rule",
            bases=(Rule,),
            dict={
                "__check__": cls.check,
                "description": cls.description,
                "supports": cls.supports
            }
        )
        cls.config = cls.config | config
        cls.priority = priority
        Rule._registry.append(cls)
        return cls
    return inner