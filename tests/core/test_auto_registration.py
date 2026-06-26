from fastapi_doctor.core.auto_registration import rule
from fastapi_doctor.core.protocol import Rule, RouteInfo
import pytest


def test_valid_class_auto_registration():
    @rule()
    class ValidRule():
        def __call__(self, route: RouteInfo):
            ...

        @property
        def description(self):
            ...

        def supports(self, route: RouteInfo):
            ...
    valid_rule = ValidRule()
    assert ValidRule in Rule._registry

    valid_rule(None)
    valid_rule.description
    valid_rule.supports(None)


def test_invalid_class_auto_registration():
    @rule()
    class InvalidRule():
        ...

    assert InvalidRule in Rule._registry
    with pytest.raises(TypeError):
        invalid_rule = InvalidRule()


def test_rule_function_parameters():
    @rule(config={"123": "abc", "priority": 4})
    class ValidRule():
        def __call__(self, route: RouteInfo):
            ...

        @property
        def description(self):
            ...

        def supports(self, route: RouteInfo):
            ...

    assert ValidRule in Rule._registry
    assert ValidRule.config == {"123": "abc", "priority": 4}
    assert ValidRule.priority == 4
