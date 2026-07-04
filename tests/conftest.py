from __future__ import annotations
from fastapi_doctor.core.protocol import RouteInfo, Issue, Rule
from functools import partial
from typing import Callable, Literal, Any
from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

@pytest.fixture
def test_client_factory(
    anyio_backend_name: Literal["asyncio", "Trio"],
    anyio_backend_options: dict[str, Any]
):
    return partial(
        TestClient,
        backend=anyio_backend_name,
        backend_options=anyio_backend_options 
    )


@pytest.fixture(autouse=True)
def clear_rule():
    Rule._registry.clear()


@pytest.fixture
def rule_subclass_factory(
    rule_call_method,
    rule_description_property,
    rule_supports_method
) -> Callable[[], type[TestRule]]:
    def _call(*, depend_on_ast: bool = False) -> type[TestRule]:
        class TestRule(Rule, depend_on_ast=depend_on_ast):
            def __call__(self, _: RouteInfo) -> Issue:
                return rule_call_method

            @property
            def description(self) -> str:
                return rule_description_property

            def supports(self, _: RouteInfo) -> bool:
                return rule_supports_method
        return TestRule
    return _call


@pytest.fixture
def rule_call_method() -> Issue:
    issue: Issue = {
        "type": "Issue",
        "level": "architectur",
        "issue": "missing_response_model",
        "methods": ["GET"],
        "categories": ["architecture"],
        "hint": "suggest adding missing response model",
    }
    return issue


@pytest.fixture
def rule_description_property() -> str:
    return "123"


@pytest.fixture
def rule_supports_method() -> bool:
    return True

@pytest.fixture
def sample_app() -> FastAPI:
    app = FastAPI()

    @app.get("/foo")
    def foo(): ...

    @app.api_route("/fizz", methods=["GET", "POST"])
    def fizz(): ...

    @app.api_route("/buzz", methods=["GET", "POST"])
    def buzz(): ...

    @app.get("/brazz")
    @app.post("/brazz")
    def brazz(): ...

    return app

@pytest.fixture
def sample_app_content() -> str:
    return (
"""
@app.get("/foo")
def foo(): ...

@app.api_route("/fizz", methods=["GET", "POST"])
def fizz(): ...

@app.api_route("/buzz", methods=["GET", "POST"])
def buzz(): ...

@app.get("/brazz")
@app.post("/brazz")
def buzz(): ...
""")
