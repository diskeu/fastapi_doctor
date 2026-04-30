from fastapi_doctor.core.protocol import RouteInfo, Issue
import pytest


@pytest.fixture
def rule_call_method(route: RouteInfo) -> Issue:
    issue: Issue = {
        "type": "Issue",
        "level": "architectur",
        "issue": "missing_response_model",
        "method": "GET",
        "category": "architecture",
        "hint": "suggest adding missing response model",
        "route": route
    }
    return issue


@pytest.fixture
def rule_description_property() -> str:
    return "123"


@pytest.fixture
def rule_supports_method() -> bool:
    return True