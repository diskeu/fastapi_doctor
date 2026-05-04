from fastapi_doctor.core.protocol import RouteInfo
from fastapi.applications import FastAPI
from typing import TypedDict, Sequence
from pathlib import Path
import ast


class RouteVisitor(ast.NodeVisitor):
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.route_bodies: dict[tuple[str, str], ast.FunctionDef] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Checks if the function defines a *valid* `fastAPI route`,
        if True, append it to `self.route_bodies`.
        """
        path = None

        for dec in node.decorator_list:
            if isinstance(dec, ast.Call):
                if isinstance(dec.func, ast.Attribute):
                    if (dec.func.value.id == self.app_name):   # type: ignore[attr-defined]
                        methods = []

                        if dec.func.attr != "api_route":
                            methods = [dec.func.attr] 

                        if hasattr(dec, "args"):
                            path = dec.args[0].value            # type: ignore[attr-defined]

                        if hasattr(dec, "keywords"):
                            for keyword in dec.keywords:
                                if keyword.arg == "path":
                                    path = keyword.value.value # type: ignore[attr-defined]
                                
                                # Handlers can be also defined with
                                # @app.api_route("/", methods=["GET", "POST"])
                                elif keyword.arg == "methods":
                                    methods.extend(
                                        const.value for const
                                        in keyword.value.elts  # type: ignore[attr-defined]
                                    )

                        if methods and path:
                            for method in methods:
                                self.route_bodies[(method, path)] = node


def extract_route_bodies(
    location: Path | str | None,
    app_name: str,
    *,
    debug_content: str = ""
) -> dict[tuple[str, str], ast.FunctionDef]:

    if isinstance(location, str):
        location = Path(location)

    content = location.read_text(encoding="utf-8") if location else debug_content
         
    tree = ast.parse(
        source=content,
        mode="exec",
        feature_version=(3, 13)
    )
    route_visitor = RouteVisitor(app_name=app_name)
    route_visitor.visit(tree)
    
    return route_visitor.route_bodies
