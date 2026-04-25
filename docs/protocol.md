`Protocols` are a simple contract, that give info on how specific
objects like `Issues` or `Rules` need to look like. The
implementation is based on the `abc` module, instead of the more
permissive `protocol` class.

# Rule
Rule is a global class that holds a list of `Rule-Subclasses` and
is a protocol with some logik behind it to keep track on all the definied
Rules.
For a a convinience behaviour when a new subclass is made, `_registry`
stays the same among diffrent instances of `Rule`.

`Rules` need to provide the following things
- a __call__ method that returns a `Issue`
- a description method that returns a string telling what the Rule does
- a `supports` method that needs to to have a route as input, returning a bool
  on wheter the Route is supported.
when inheriting from the `Rules` class you can provide optional configuration via `kwargs`

```python
from fastapi_doctor.core.protocol import Rule

class MissingResponseModel(Rule, priority=4):
    def __call__(self, route):
        # logik
        ... # -> should return Issue

    def description(self) -> str:
        return "What the Route does"
    
    def supports(self, Route) -> bool:
        # validating if the given Route is supported
        return True
``` 

    