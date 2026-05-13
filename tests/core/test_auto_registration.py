from fastapi_doctor.core.auto_registration import rule
from fastapi_doctor.core.protocol import Rule, RouteInfo


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


def test_invalid_class_auto_registration_():
    ...


def test_rule_function_parameters():
    ...


def test_class_declaration_values_overwrite():
    """
    Test declaring `config and priority` in class and overwritting
    them with the `rule` decorator function parameters.
    """
    ...

