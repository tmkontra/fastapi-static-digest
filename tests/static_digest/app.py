from pathlib import Path

from fastapi import FastAPI
from fastapi_static_digest import StaticDigest


app_root = Path(__file__).parent

def create_app():
    app = FastAPI()
    static = StaticDigest(directory=app_root / "static")
    app.mount("/static", static)
    return app