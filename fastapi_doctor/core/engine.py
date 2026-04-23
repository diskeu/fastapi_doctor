from typing import Callable, Any
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from enum import Enum
from fastapi.applications import FastAPI
from fastapi.routing import APIRoute


@dataclass
class RouteInfo():
    path: str
    endpoint: Callable[..., Any]
    name: str

    # Optional Metadata
    methods: Collection[str] | None = None
    status_code: int | None = None
    response_model: Any | None = None
    summary: str | None = None
    description: str | None = None
    tags: list[str | Enum] | None = None
    deprecated: bool | None = None
    strict_content_type: bool = True
    include_in_schema: bool = True

    @property
    def auto_generated_name(self) -> bool:
        return self.name == self.endpoint.__name__


def extract_routes(app: FastAPI) -> Sequence[RouteInfo]:
    routes: list = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append(
                RouteInfo(
                    path=route.path,
                    endpoint=route.endpoint,
                    name=route.name,

                    # Optional Metadata
                    methods=route.methods,
                    status_code=route.status_code,
                    response_model=route.response_model,
                    summary=route.summary,
                    description=route.description,
                    tags=route.tags,
                    deprecated=route.deprecated,
                    strict_content_type=route.strict_content_type,
                    include_in_schema=route.include_in_schema,
                )
            )
    return routes