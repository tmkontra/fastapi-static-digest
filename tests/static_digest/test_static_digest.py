from os import DirEntry
from pathlib import Path
from fastapi_static_digest import StaticDigest, StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient

from .app import app_root, create_app


@pytest.fixture()
def client():
    """Fixture to execute asserts before and after a test is run"""
    compiler = StaticDigestCompiler(app_root / "static")
    compiler.compile()
    client = TestClient(create_app())
    yield client
    compiler.clean()

def test_manifest(client):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    original = client.get("/static/data.json")
    assert original.status_code == 200
    digested = client.get(f"/static/_digest/{digested_name}")
    assert digested.status_code == 200
    oj = original.json()
    dj = digested.json()
    assert oj == dj



    
    
    
