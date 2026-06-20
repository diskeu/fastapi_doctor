from fastapi_doctor.core.executor import Executor

from json import loads
from typing import Any
from fastapi_doctor.core.protocol import Issue


def assert_issue_output_summary(summary: dict[str, int | list[str]]) -> None:
    ...


def assert_issue_output_routes(routes: list[dict[str, Any]]) -> None:
    ...


def assert_issue_output_rule_issues(rule_issues: dict[str, list[Issue]]) -> None:
    ...


def test_executor_issue_output() -> None:
    ...


def test_executor_json_output_env() -> None:
    ...


def test_executor_json_output_file() -> None:
    ...
