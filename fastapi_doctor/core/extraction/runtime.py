from typing import Iterator
from fastapi.applications import FastAPI
from fastapi.routing import APIRoute
from fastapi_doctor.core.protocol import RouteInfo

# iter_route_contexts is only supported in fastapi >= 0.137.2
# since `app.routes` got refactored in 0.137.0, version 0.137.0
# and 0.137.1 are not supported
try:
    from fastapi.routing import iter_route_contexts
    from starlette.routing import BaseRoute

    def _iter_api_routes(app: FastAPI) -> Iterator[APIRoute]:
        for ctx in iter_route_contexts(app.routes):
            route: BaseRoute = ctx.original_route
            if isinstance(route, APIRoute):
                yield route

except ImportError:

    def _iter_api_routes(app: FastAPI) -> Iterator[APIRoute]:
        for route in app.routes:
            print("ROUTE ", route)
            if isinstance(route, APIRoute):
                yield route
        # return (
        #     route for route in app.routes
        #     if isinstance(route, APIRoute)
        # )


def extract_routes(app: FastAPI) -> list[RouteInfo]:
    routes: list = []
    for route in _iter_api_routes(app):
        routes.append(
            RouteInfo(
                path=route.path,
                endpoint=route.endpoint,
                name=route.name,
                methods=route.methods,

                # Optional Metadata
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