from collections.abc import Sequence
from fastapi.applications import FastAPI
from fastapi.routing import APIRoute
from fastapi_doctor.core.protocol import RouteInfo


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