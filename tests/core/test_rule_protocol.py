from fastapi_doctor.core.protocol import Rule, RouteInfo, Issue
import pytest

def test_add_invalid_rule(
    rule_call_method,
    rule_description_property,
    rule_supports_method
):

    class MissingCallRule(Rule):
        # missing `__call__` method

        @property
        def description(self) -> str:
            return rule_description_property

        def supports(self, _: RouteInfo) -> bool:
            return rule_supports_method
        
    with pytest.raises(TypeError):
        MissingCallRule()


    class MissingDescriptionRule(Rule):
        def __call__(self, route: RouteInfo) -> Issue:
            return rule_call_method
        
        # missing `description`

        def supports(self, _: RouteInfo) -> bool:
            return rule_supports_method
        
    with pytest.raises(TypeError):
        MissingDescriptionRule()
    

    class MissingSupportsRule(Rule):
        def __call__(self, route: RouteInfo) -> Issue:
            return rule_call_method

        @property
        def description(self) -> str:
            return rule_description_property

        # missing `supports` method

    with pytest.raises(TypeError):
        MissingSupportsRule()