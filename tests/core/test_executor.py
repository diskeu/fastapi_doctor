from fastapi_doctor.core.executor import Executor

import pytest
from json import loads
from typing import Callable, Any
from pathlib import Path
from fastapi import FastAPI
from fastapi_doctor.core.protocol import Issue, Rule
from fastapi_doctor.core.executor import Executor


def assert_issue_output_summary(summary: dict[str, int | list[str]]) -> None:
    ...


def assert_issue_output_routes(routes: list[dict[str, Any]]) -> None:
    ...


def assert_issue_output_rule_issues(rule_issues: dict[str, list[Issue]]) -> None:
    ...


def test_executor_issue_output(
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

    assert_issue_output_summary(issues["summary"])
    assert_issue_output_routes(issues["routes"])
    assert_issue_output_rule_issues(issues["rule_issues"])


def test_executor_json_output_env() -> None:
    ...


def test_executor_json_output_file() -> None:
    ...