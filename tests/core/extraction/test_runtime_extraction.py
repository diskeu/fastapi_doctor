from typing import Callable
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from fastapi import APIRouter
from fastapi_doctor.core.extraction.runtime import (
    extract_routes,
    RouteInfo
)


def test_extract_routes() -> None:
    router = APIRouter()
    @router.get("/")
    def foo():
        return {"123": "abc"}
    @router.get("/fizz")
    def fizz():
        return {"123": "abc"}

    app = FastAPI()
    app.include_router(router)
    routes = extract_routes(app)

    assert routes
    for route in routes:
        assert isinstance(route, RouteInfo)
        assert isinstance(route.path, str)
        assert isinstance(route.endpoint, str)
        assert isinstance(route.name, str)