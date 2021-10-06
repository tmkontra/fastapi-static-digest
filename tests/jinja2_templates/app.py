from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi_static_digest import StaticDigest


app_root = Path(__file__).parent

def create_app():
    app = FastAPI()
    static = StaticDigest(directory=app_root / "static")
    templates = Jinja2Templates(app_root / "templates")
    static.register_static_url_for(templates)
    @app.get("/")
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    app.mount("/static", static)
    return app