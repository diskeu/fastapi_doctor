from typing import Sequence
from fastapi_doctor.core.protocol import RouteInfo
from ast import FunctionDef

def merge(route_infos: Sequence[RouteInfo], route_bodies: dict[tuple[str, str], FunctionDef]) -> None:
    """
    Enriches/Merges the `route_infos` with `route_bodies`
    """
    for route in route_infos:
        route.body = {}
        for method in route.methods:
            ast_handler_body: FunctionDef | None = route_bodies.get((method, route.path))
            # TODO: raise an exception if `ast_handler_body` is None
            route.body[method] = ast_handler_body # type: ignore[assignment]
