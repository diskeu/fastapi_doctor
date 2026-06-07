## auto_registration
Rules can be also created via defining a normal class that has
`__call__`, `description` and `supprots` method and using the `@rule`
decorator. `config` can still be created via parsing it
as keyword arguments to the decorator. `priority` and `depend_on_ast`
are extracted from config.
```python
from fastapi_doctor.core.protocol import Issue

@rule(config={"abc": 123, "priority": 4, "depend_on_ast": True})
class MissingResponseModel():
    def __call__(self, route) -> Issue | None:
        # logik
        ...

    def description(self) -> str:
        return "What the Route does"
    
    def supports(self, Route) -> bool:
        # validating if the given Route is supported
        return True
```
