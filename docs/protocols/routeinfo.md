# RouteInfo
Fastapi-doctor uses its own `RouteInfo` dataclass for a simpler abstraction
of FastAPI's `APIRoute` class and can also contain `ast FunctionDef` nodes
when `depends_on_ast` is enabled, (See [Rule](rule.md) and
[AutoRegistration](auto_registration.md)).
The class is in contrast to the `APIRoute` class only for holding data,
doesn't has any logic and only has fields that are necessary for `Rule`'s.
