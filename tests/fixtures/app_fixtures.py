from functools import partial
from typing import Literal, Any
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def test_client_factory(
    anyio_backend_name: Literal["asyncio", "Trio"],
    anyio_backend_options: dict[str, Any]
):
    return partial(
        TestClient,
        backend=anyio_backend_name,
        backend_options=anyio_backend_options 
    )
