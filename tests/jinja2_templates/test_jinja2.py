
from fastapi_static_digest import StaticDigestCompiler
import pytest
from fastapi.testclient import TestClient
from urllib.parse import urlparse

from .app import app_root, create_app, static_source_dir


@pytest.fixture()
def client():
    """Fixture to execute asserts before and after a test is run"""
    compiler = StaticDigestCompiler(source_directory=static_source_dir)
    compiler.compile()
    client = TestClient(create_app())
    yield client
    compiler.clean()

def test_static_url_for(client: TestClient):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    response = client.get("/")
    assert response.status_code == 200
    static_url = f"/static/{digested_name}"
    url = urlparse(response.text)
    assert url.path == static_url



    
    
    
