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


# RouteInfo
Fastapi-doctor uses its own `RouteInfo` dataclass for a simpler abstraction
of FastAPI's `APIRoute` class.
The class is in contrast to the `APIRoute` class only for holding data,
doesn't has any logic and only has necessary fields from the original class.


# Issue
A `Issue` is the defined type a `Rule` returns when an `Issue` in the given route
occures. It is built with inheriting from the permissive `TypedDict` class.
To define an `Issue` the following fields need to be in the with `:issue` annotated
dictionary:
    ** type: str **               -> the type of the dictionary [normally set to "Issue"],
                                     identifies it from other dictionaries
    ** level: str **              -> the name of the vulnerability level
    ** issue: str **              -> the name of the issue itself
    ** methods: list[str] **      -> the methods that cause the issue
    ** categories: list[str] **   -> the categories in which the issue fits
    ** hint: str **               -> a hint for the AI

    Fields that should not be set [will be overwritten]:
    route_info: NotRequired[dict[Any, Any]] -> the route_info in dictionary format
Code Example:
```python
    issue: Issue = {
        "type": "Issue",
        "level": "architectur",
        "issue": "missing_response_model",
        "methods": ["GET"],
        "categories": ["architecture", "unlocated"],
        "hint": "suggest adding missing response model for the specific methods",
    }
```