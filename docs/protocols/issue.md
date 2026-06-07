# Issue
A `Issue` is the defined type a `Rule` returns when an `Issue` in the given route
occures. It is built with inheriting from the permissive `TypedDict` class.
To define an `Issue` the following fields need to be in the with `:issue` annotated
dictionary:
| Field | Description |
|---------|-------------|
| `type: str` | the type of the dictionary |
| `level: str` | the name of the vulnerability level |
| `issue: str` | the name of the issue itself |
| `methods: list[str]` | the methods that cause the issue |
| `categories: list[str]` | the categories in which the issue fits |
| `hint: str` | a hint for the AI |
| `route_info: NotRequired[dict[Any, Any]]` | overwritten automatically |

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
