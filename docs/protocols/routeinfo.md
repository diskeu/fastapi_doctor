# RouteInfo
Fastapi-doctor uses its own `RouteInfo` dataclass for a simpler abstraction
of FastAPI's `APIRoute` class.
The class is in contrast to the `APIRoute` class only for holding data,
doesn't has any logic and only has necessary fields from the original class.
