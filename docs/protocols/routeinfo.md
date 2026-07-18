# RouteInfo
Fastapi-doctor uses its own `RouteInfo` dataclass for a simpler abstraction
of FastAPI's `APIRoute` class and can also contain `ast FunctionDef` nodes
when `depends_on_ast` is enabled, (See [Rule](rule.md) and
[AutoRegistration](auto_registration.md)).
The class is in contrast to the `APIRoute` class only for holding data,
doesn't has any logic and only has fields that are necessary for `Rule`'s.

## Fields of `RouteInfo` (`route` is meant as FastAPI's `APIRoute`):
| Field | Description |
| ----- | ----------- |
| `path: str` | similar to `route.path` |
| `endpoint: str` | endpoint_method.__name__ |
| `name: str` | similar to `route.name` |
| `methods: Collection[str]` | similar to `route.methods` |
## Optional Metadata (Can be None if not bool, always similar to route.<field>)
+ status_code: int
+ response_model: Any
+ summary: str
+ description: str
+ tags: list[str | Enum]
+ deprecated: bool
+ strict_content_type: bool = True
+ include_in_schema: bool = True
+ body: dict[str, FunctionDef] > Optional ast-Route-Information
