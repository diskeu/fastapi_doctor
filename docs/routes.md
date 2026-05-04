# etract_routes
Converts FastAPI routes to `RouteInfo` instances.

# extract_route_bodies
Underlying function that calls `RouteVisitor().visit()` and returns
`dict[tuple[method, path], ast.FunctionDef]`. `Ast.FunctionDef` is the
function definition node that holds all static ast information about the
Route function.
