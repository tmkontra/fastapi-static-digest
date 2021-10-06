from pathlib import Path

from fastapi import FastAPI
from fastapi import staticfiles
from fastapi.staticfiles import StaticFiles
from fastapi_static_digest import StaticDigest, StaticDigestCompiler


app_root = Path(__file__).parent

static_input_dir = app_root / "static"

def create_app(output_dir=None):
    app = FastAPI()
    if output_dir is not None:
        static_digest = StaticDigest(static_dir=output_dir)
        static = StaticFiles(directory=static_digest.directory)
    else:
        static_digest = StaticDigest(source_dir=static_input_dir)
        static = StaticFiles(directory=static_digest.directory)
    app.mount("/static", static, name="static")
    return app