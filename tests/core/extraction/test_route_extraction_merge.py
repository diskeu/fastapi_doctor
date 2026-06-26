from fastapi_doctor.core.extraction.runtime import extract_routes
from fastapi_doctor.core.extraction.ast_enrich import extract_route_bodies
from fastapi_doctor.core.protocol import RouteInfo
from fastapi_doctor.core.merge import merge
from fastapi import FastAPI
from ast import FunctionDef

def test_route_extraction_merge(sample_app, sample_app_content) -> None:

    route_infos = extract_routes(sample_app) 
    route_bodies = extract_route_bodies(
        location=None,
        app_name="app",
        debug_content=sample_app_content
    )
    merge(
        route_infos=route_infos,
        route_bodies=route_bodies
    )
    for route in route_infos:
        assert isinstance(route, RouteInfo)
        assert isinstance(route.path, str)
        assert callable(route.endpoint)
        assert isinstance(route.name, str)
        for method in route.methods:
            assert isinstance(route.body[method], FunctionDef)