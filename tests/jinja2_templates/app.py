from os import name
from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from fastapi_static_digest import StaticDigest


app_root = Path(__file__).parent

static_source_dir = app_root / "static_files"
static_dir = app_root / "static_digest"

def create_app():
    app = FastAPI()
    static_files = StaticFiles(directory=static_dir)
    templates = Jinja2Templates(app_root / "templates")
    static_digest = StaticDigest(static_dir)
    static_digest.register_static_url_for(templates)
    @app.get("/")
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    app.mount("/static", static_files, name="static")
    return app