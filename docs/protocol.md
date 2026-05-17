`Protocols` are a simple contract, that give info on how specific
objects like `Issues` or `Rules` need to look like. They can be for
real validation of the correct fields or for development experience with
a more permissive implemantation.


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
## auto_registration
Rules can be also created via defining a normal class that has
`__call__`, `description` and `supprots` method and using the `@rule`
decorator. `priority` and `config` can still be created via parsing them
as keyword arguments to the decorator.
```python
from fastapi_doctor.core.protocol import Issue

@rule(config={"abc": 123}, priority=4, depend_on_ast=True)
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


# RouteInfo
Fastapi-doctor uses its own `RouteInfo` dataclass for a simpler abstraction
of FastAPI's `APIRoute` class.
The class is in contrast to the `APIRoute` class only for holding data,
doesn't has any logic and only has necessary fields from the original class.


# Issue
A issue is the defined type a `Rule` returns when an `issue` in the given route
occures. It is built with inheriting from the permissive `TypedDict` class and
doesn't has any real affect in the code execution.