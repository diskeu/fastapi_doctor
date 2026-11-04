# FastAPI Doctor

FastAPI Doctor is a plugin-based security analysis tool for FastAPI applications. It detects potential vulnerabilities and misconfigurations
through an extensible rule system that allows developers to define their own checks appropriate to their projects.

FastAPI Doctor != Classic Unit Tests

Traditional unit tests are essential for verifying application logic, but they don’t always cover security vulnerabilities, architectural issues,
or framework-specific misconfigurations.

FastAPI Doctor aims to fill this gap by providing an additional layer of application-specific analysis.
Instead of testing individual functions or endpoints in isolation, FastAPI Doctor analyzes the routes of your FastAPI application and executes
your rules against them.

This makes it possible to implement checks that go beyond traditional testing due providing things as Abstract Syntacs tree view of the function.
This also make it possible to integrate a LLM inside your rule which directly gets the AST information about the function.

## How It Works

FastAPI Doctor discovers and analyzes the routes registered in your FastAPI application. Each route is represented through FastAPI Doctor’s own
abstraction layer, providing a consistent interface for custom rules.

The analysis engine executes every registered rule against the discovered routes. Rules can inspect route information and, when configured,
access additional information such as the AST of the underlying endpoint.
Whenever a rule detects something suspicious, it produces an Issue containing information about the finding.

## Extensibility

FastAPI Doctor is designed around a plugin-based architecture.
You can implement your own rules to enforce application-specific requirements or detect vulnerabilities that generic security tools might not know about.
Due the plugins, you can extend the analysis engine without having to modify its core implementation.

The different abstractions FastAPI Doctor uses can be located in the according documentation.
FastAPI Doctor provides detailed documentation explaining all the things the end user needs to know about.
