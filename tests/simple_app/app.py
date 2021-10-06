from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app_root = Path(__file__).parent

app = FastAPI()

static = StaticFiles(directory=app_root / "static")

app.mount("/static", static)