from fastapi_doctor.core.protocol import Rule, RouteInfo, Issue
import pytest


def test_rule_iter_registry(rule_subclass_factory):
    test_rule1 = rule_subclass_factory()  
    test_rule2 = rule_subclass_factory()
    rules_generator = Rule.iter_registry()

    assert next(rules_generator) is test_rule1
    assert next(rules_generator) is test_rule2


def test_rule_iter_registry_sorted(rule_subclass_factory):
    test_rule1 = rule_subclass_factory()  
    test_rule2 = rule_subclass_factory()
    test_rule1.priority, test_rule2.priority = 8, 4

    rules_generator = Rule.iter_registry_sorted()

    assert next(rules_generator) is test_rule2
    assert next(rules_generator) is test_rule1


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