from fastapi.applications import FastAPI
# iter_route_contexts is only supported in fastapi >= 0.137.2
from fastapi.routing import APIRoute, iter_route_contexts
from fastapi_doctor.core.protocol import RouteInfo
from starlette.routing import BaseRoute


def extract_routes(app: FastAPI) -> list[RouteInfo]:
    routes: list = []

    for ctx in iter_route_contexts(app.routes):
        route: BaseRoute = ctx.original_route
        if isinstance(route, APIRoute):
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