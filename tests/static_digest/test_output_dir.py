import json
from os import DirEntry
from pathlib import Path
from fastapi_static_digest import StaticDigest, StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient

from .app.app import app_root, create_app, static_input_dir


rel_static_output = "../static_digest"

@pytest.fixture()
def client():
    """Fixture to execute asserts before and after a test is run"""
    output = static_input_dir / rel_static_output
    compiler = StaticDigestCompiler(static_input_dir, output_dir=output)
    compiler.compile()
    client = TestClient(create_app(output))
    yield client
    compiler.clean()

def test_output_dir(client):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    original = client.get("/static/data.json")
    assert original.status_code == 404
    digested = client.get(f"/static/{digested_name}")
    assert digested.status_code == 200
    assert digested.json() == {"key": "value"}

    
    
    