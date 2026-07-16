from fastapi_doctor.core.executor import Executor

from json import loads
from typing import Any
from fastapi_doctor.core.protocol import Issue
from fastapi_doctor.core.executor import Executor


def assert_issue_output_summary(
        summary: dict[str, list[str | int]],
        with_ast: bool = False
    ) -> None:

    # Different methods on the same route are counted as one route with different
    # methods. See class `RouteInfo`!
    assert summary["total_routes"] == 5
    assert summary["total_rules"] == 2

    # `AST` is not supported by one of the sample rules
    assert summary["issues_collected"] == 5 if not with_ast else 10
    assert len(summary["skipped_rules"]) == (1 if not with_ast else 0)


def assert_issue_output_routes(
        routes: list[dict[str, Any]],
        with_ast: bool = False
    ) -> None:
    ...


def assert_issue_output_rule_issues(
        rule_issues: dict[str, list[Issue]],
        with_ast: bool = False
    ) -> None:
    ...


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
    assert_issue_output_routes(issues["routes"], with_ast=True)
    assert_issue_output_rule_issues(issues["rule_issues"], with_ast=True)


def test_executor_json_output_env() -> None:
    ...


def test_executor_json_output_file() -> None:
    ...