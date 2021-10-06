import json
from os import stat
from pathlib import Path

from fastapi.staticfiles import StaticFiles
import jinja2
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fastapi_static_digest.compiler import StaticDigestCompiler


class StaticDigest:
    def __init__(self, source_dir=None, static_dir=None):
        if source_dir is not None:
            self.directory = StaticDigestCompiler.default_output_dir(source_dir)
        elif static_dir is not None:
            self.directory = static_dir
        else:
            raise ValueError("Must provide one of 'source_dir' or 'output_dir'")
        self.manifest_file = Path(self.directory) / "cache_manifest.json"
        self.manifest = self.load_manifest()

    def load_manifest(self):
        with open(self.manifest_file, "r") as f:
            return json.load(f)

    def register_static_url_for(self, templates: Jinja2Templates):
        @jinja2.contextfunction
        def static_url_for(context, name, path=None) -> str:
            request: Request = context["request"]
            digested_path = self.manifest[path]
            return request.url_for(name, path=digested_path)
        templates.env.globals['static_url_for'] = static_url_for
