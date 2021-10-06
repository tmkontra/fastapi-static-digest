
from fastapi_static_digest import StaticDigestCompiler
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

def test_static_url_for(client: TestClient):
    digested_name = "data.316447ed7921f01abb8e798be0c41f60.json"
    response = client.get("/")
    assert response.status_code == 200
    static_url = f"/static/_digest/{digested_name}"
    assert response.text == static_url



    
    
    
