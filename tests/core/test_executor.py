from fastapi_doctor.core.executor import Executor

from json import loads
from typing import Any
from fastapi_doctor.core.protocol import Rule, Issue
from fastapi_doctor.core.executor import Executor


def assert_issue_output_summary(
        summary: dict[str, list[str | int]],
        with_ast: bool = False
    ) -> None:

    # Different methods on the same route are counted as one route with different
    # methods. See class `RouteInfo`!
    assert summary["total_routes"] == 5
    assert summary["total_rules"] == len(list(Rule.iter_registry()))

    # `AST` is not supported by one of the sample rules
    assert summary["issues_collected"] == 5 if not with_ast else 10
    assert len(summary["skipped_rules"]) == (1 if not with_ast else 0)


def assert_issue_output_rule_issues(
        rule_issues: dict[str, list[Issue]]
    ) -> None:
    for rule in Rule.iter_registry_sorted():
        issues = rule_issues[rule.name]

        for issue in issues:
            assert type(issue["type"]) == str
            assert type(issue["level"]) == str
            assert type(issue["hint"]) == str
            assert type(issue["route_info"]) == dict

            assert type(issue["methods"]) == list
            methods: set[type] = {type(method) for method in issue["methods"]}
            assert methods == {str}

            assert type(issue["categories"]) == list
            categories: set[type] = {type(category) for category in issue["categories"]}
            assert categories == {str}


def assert_issue_output_routes(
        routes: list[dict[str, Any]]
    ) -> None:
    for route in routes:
        assert isinstance(route, dict)
        assert isinstance(route["path"], str)
        assert isinstance(route["endpoint"], str)
        assert isinstance(route["name"], str)


def test_executor_issue_output_without_ast(
        sample_app,
        rule_subclass_factory
):
    rule_subclass_factory(depend_on_ast=False)
    rule_subclass_factory(depend_on_ast=True)
    
    json_issue_output = Executor(sample_app)()
    issues = loads(json_issue_output)

    assert_issue_output_summary(issues["summary"])
    assert_issue_output_routes(issues["routes"])
    assert_issue_output_rule_issues(issues["rule_issues"])


def test_executor_issue_output_with_ast(
    sample_app,
    sample_app_content,
    rule_subclass_factory,
    tmp_path
) -> None:
    rule_subclass_factory(depend_on_ast=False)
    rule_subclass_factory(depend_on_ast=True)

    d = tmp_path / "sample_app_content"
    d.mkdir()
    p = d / "sample_app_content.py"
    p.write_text(sample_app_content)

    json_issues_output = Executor(
        sample_app,
        {"location": str(p), "app_name": "app"}
    )()
    issues = loads(json_issues_output)

    assert_issue_output_summary(issues["summary"], with_ast=True)
    assert_issue_output_rule_issues(issues["rule_issues"])
    assert_issue_output_routes(issues["routes"])


def test_executor_json_output_env() -> None:
    ...


def test_executor_json_output_file() -> None:
    ...