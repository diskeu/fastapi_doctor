from fastapi_doctor.core.extraction.ast_enrich import extract_route_bodies
from fastapi_doctor.core.extraction.runtime import extract_routes
from fastapi_doctor.core.merge import merge
from fastapi_doctor.core.protocol import Rule, RouteInfo, Issue
from fastapi import FastAPI
from typing import Sequence, Any
from collections import defaultdict
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
        routes: list[RouteInfo] = extract_routes(self.app)
        skipped_rules: list[str] = []
        rules_issue_mapping: dict[str, list[Issue]] = defaultdict(list)
        len_issues: int = 0

        routes_asdict: list[dict[str, Any]] = [
            asdict(route) for route in routes
        ]

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
            if not rule.depend_on_ast or self.ast_enrichment:
                rule_instance = rule()
                for route, route_asdict in zip(routes, routes_asdict):
                    if rule_instance.supports(route):
                        if returned_issue := rule_instance(route):
                            returned_issue["route_info"] = route_asdict
                            rules_issue_mapping[rule.name].append(returned_issue)
                            len_issues += 1
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
                    "issues_collected": len_issues,
                    "skipped_rules": skipped_rules
                },
                "rule_issues": rules_issue_mapping,
                # routes in json need to be converted into a simple dict
                "routes": routes_asdict
            },
            default=list
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