import os
from pathlib import Path
from fastapi_static_digest import StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient

from . import get_json
from .app.app import create_app, static_input_dir


output_relpath = "../static_digest"
output_dir = static_input_dir / output_relpath
compiler = StaticDigestCompiler(static_input_dir, output_dir=output_dir)
assert compiler.output_directory == output_dir

@pytest.fixture(scope="function")
def client():
    """Fixture to execute asserts before and after a test is run"""
    compiler.compile()
    client = TestClient(create_app(output_dir))
    yield client
    compiler.clean()

def test_output_dir(client):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    original = client.get("/static/data.json")
    assert original.status_code == 404
    digested = client.get(f"/static/{digested_name}")
    assert digested.status_code == 200
    assert digested.json() == {"key": "value"}
    manifest = get_json(output_dir / "cache_manifest.json")
    visited = 0
    for (dirpath, _, filenames) in os.walk(static_input_dir):
        with pytest.raises(ValueError):
            Path(dirpath).relative_to(output_dir)    
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