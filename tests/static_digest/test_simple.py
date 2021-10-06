import json
import os
from pathlib import Path
from fastapi_static_digest import StaticDigest, StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient

from . import get_json
from .app.app import app_root, create_app, static_input_dir


compiler = StaticDigestCompiler(static_input_dir)
output_dir = compiler.output_directory

@pytest.fixture(scope="function")
def client():
    """Fixture to execute asserts before and after a test is run"""
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
    manifest = get_json(output_dir / "cache_manifest.json")
    visited = 0
    for (dirpath, _, filenames) in os.walk(static_input_dir):
        try:
            Path(dirpath).relative_to(output_dir)
            continue
        except ValueError:
            pass
        for filename in filenames:
            abspath = Path(dirpath) / filename
            relpath = abspath.relative_to(static_input_dir)
            outpath = manifest[str(relpath)]
            digested_abspath = output_dir / outpath
            with open(abspath, "rb") as src:
                with open(digested_abspath, "rb") as dig:
                    assert src.read() == dig.read()
            visited += 1
    assert visited == len(manifest)