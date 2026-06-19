from fastapi_doctor.core.extraction.ast_enrich import extract_route_bodies
from fastapi import APIRouter
from fastapi.applications import FastAPI


def test_extract_route_bodies():
    app_content = (
"""
@app.get("/foo")
def foo(): ...

@app.api_route("/fizz", methods=["GET", "POST"])
def fizz(): ...

@app.get("/")
@app.api_route("/buzz", methods=["GET", "POST"])
def buzz(): ...

@app.get("/brazz")
@app.post("/brazz")
def foo(): ...
""")
    bodies = extract_route_bodies(
        location=None,
        app_name="app",
        debug_content=app_content
    )
    assert bodies["GET", "/foo"]
    assert bodies["GET", "/fizz"]
    assert bodies["POST", "/fizz"]
    assert bodies["GET", "/buzz"]
    assert bodies["POST", "/buzz"]
    assert bodies["GET",  "/brazz"]
    assert bodies["POST",  "/brazz"]