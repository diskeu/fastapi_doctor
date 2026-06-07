# Rule
Rule is a global class that holds a list of `Rule-Subclasses` and
is a protocol with some logik behind it to keep track on all the definied
Rules.
The implementation is based on the `abc` module, instead of the more
permissive `protocol` class.
For a a convinience behaviour when a new subclass is made, `_registry`
stays the same among diffrent instances of `Rule`.

`Rules` need to provide the following things
- a __call__ method that returns a `Issue` or `None` if no vulerability is found
- a description method that returns a string telling what the Rule does
- a `supports` method that needs to to have a route as input, returning a bool
  on wheter the Route is supported.
when inheriting from the `Rules` class you can provide optional configurations
via `kwargs`

```python
from fastapi_doctor.core.protocol import Rule, Issue

class MissingResponseModel(Rule, priority=4, depend_on_ast=True):
    def __call__(self, route) -> Issue | None:
        # logik
        ...

    def description(self) -> str:
        return "What the Route does"
    
    def supports(self, Route) -> bool:
        # validating if the given Route is supported
        return True
```
