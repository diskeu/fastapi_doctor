from fastapi_doctor.core.protocol import Rule, RouteInfo, Issue
import pytest


def test_add_invalid_rule():

    class MissingCallRule(Rule):
        # missing `__call__` method

        @property
        def description(self) -> str:
            return "123"

        def supports(self, _: RouteInfo) -> bool:
            return False
        
    with pytest.raises(TypeError):
        MissingCallRule()


    class MissingDescriptionRule(Rule):
        def __call__(self, route: RouteInfo) -> Issue:
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
        
        # missing `description`

        def supports(self, _: RouteInfo) -> bool:
            return False
        
    with pytest.raises(TypeError):
        MissingDescriptionRule()
    

    class MissingSupportsRule(Rule):
        def __call__(self, route: RouteInfo) -> Issue:
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

        @property
        def description(self) -> str:
            return "123"

        # missing `supports` method

    with pytest.raises(TypeError):
        MissingSupportsRule()