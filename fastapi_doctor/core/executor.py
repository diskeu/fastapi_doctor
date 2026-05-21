from fastapi_doctor.core.extraction.ast_enrich import extract_route_bodies
from fastapi_doctor.core.extraction.runtime import extract_routes
from fastapi_doctor.core.merge import merge
from fastapi_doctor.core.protocol import Rule, Issue
from fastapi import FastAPI
from typing import Sequence


class Executor():
    def __init__(self, app: FastAPI, /, ast_enrichment: dict[str, str] | None = None, json_output: bool = False):
        """
        Initialises an Exectur object.

        :param app: The FastAPI app
        :type app: FastAPI
        :param ast_enrichment: dictionary containing {"location": "file/to/app", "app_name"}
        :type ast_enrichment: dict[str, str]
        :param json_output: If True, the output will be written in the output file specified in the CLI-Arguments or
        JSON_OUTPUT environment variable
        :type json_output: bool
        """
        self.app = app
        self.json_output = json_output
        self.ast_enrichment = ast_enrichment

    def __call__(self):
        issues: list[Issue] = []
        routes = extract_routes(self.app)
        skipped_rules: list[type[Rule]] = []

        if self.ast_enrichment:
            merge(
                routes,
                extract_route_bodies(
                    location=self.ast_enrichment["location"],
                    app_name=self.ast_enrichment["app_name"]
                )
            )
        rule_instance: Rule
        for rule in Rule.iter_registry_sorted():
            rule_instance = rule()
            for route in routes:
                if rule.depend_on_ast == (True if self.ast_enrichment else False):
                    if rule_instance.supports(route):
                        if returned_issue := rule_instance(route):
                            issues.append(returned_issue)
                else:
                    skipped_rules.append(rule)
                    