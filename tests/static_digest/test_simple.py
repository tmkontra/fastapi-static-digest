import json
from os import DirEntry
from pathlib import Path
from fastapi_static_digest import StaticDigest, StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient

from . import get_json
from .app.app import app_root, create_app, static_input_dir


@pytest.fixture()
def client():
    """Fixture to execute asserts before and after a test is run"""
    compiler = StaticDigestCompiler(static_input_dir)
    compiler.compile()
    client = TestClient(create_app())
    yield client
    compiler.clean()

def test_manifest(client):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    original = client.get("/static/data.json")
    assert original.status_code == 404
    digested = client.get(f"/static/{digested_name}")
    assert digested.status_code == 200
    assert digested.json() == get_json(static_input_dir / "data.json")

