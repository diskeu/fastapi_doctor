from fastapi_doctor.core.protocol import RouteInfo, Issue
from functools import partial
from typing import Literal, Any
from fastapi.testclient import TestClient
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


@pytest.fixture
def rule_call_method() -> Issue:
    issue: Issue = {
        "type": "Issue",
        "level": "architectur",
        "issue": "missing_response_model",
        "method": "GET",
        "category": "architecture",
        "hint": "suggest adding missing response model",
        "route": "route"
    }
    return issue


@pytest.fixture
def rule_description_property() -> str:
    return "123"


@pytest.fixture
def rule_supports_method() -> bool:
    return True