from fastapi_doctor.core.extraction.ast_enrich import extract_route_bodies
from fastapi_doctor.core.extraction.runtime import extract_routes
from fastapi_doctor.core.merge import merge
from fastapi_doctor.core.protocol import Rule, Issue
from fastapi import FastAPI
from typing import Sequence
from pathlib import Path
from os import getenv
from dataclasses import asdict
import json


class Executor():
    def __init__(
        self,
        app: FastAPI,
        /,
        ast_enrichment: dict[str, str] | None = None,
        json_output: bool = False,
        json_output_location_arg: str | None = None
    ):
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
        if json_output_location_arg:
            self.json_output_location_arg = json_output_location_arg

    def __call__(self) -> str:
        issues: list[Issue] = []
        routes = extract_routes(self.app)
        skipped_rules: list[str] = []

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
                if rule.depend_on_ast == (True if self.ast_enrichment else False): # TODO: Potential Issue
                    if rule_instance.supports(route):
                        if returned_issue := rule_instance(route):
                            issues.append(returned_issue)
                else:
                    skipped_rules.append(rule.name)

        # Only provide necessary information, things like `executed rules`,
        # `rules skipped due no support`, can be calculated later. Provide
        # an abstract layer over the objects themselves to keep json lightweight.
        json_issues_output = json.dumps(
            {
                "summary": {
                    "total_routes": len(routes),
                    "total_rules": len(Rule._registry),
                    "issues_collected": len(issues),
                    "skipped_rules": {
                        "amount": len(skipped_rules),
                        "routes": skipped_rules
                    }
                },
                "routes": [asdict(route_info) for route_info in routes],
                # Maybe consider to make every issue part of a Rule
                "issues": issues,
                "routes": routes,
            }
        )

        # Writing json output to `json_output` file
        if self.json_output:
            output_location: Path
            if hasattr(self, "json_output_location_arg"):
                output_location = Path(self.json_output_location_arg)
            else:
                output_location = Path(getenv("JSON_OUTPUT", ""))
            if output_location:
                with open(output_location) as json_output_file:
                    json_output_file.write(json_issues_output)

        return json_issues_output