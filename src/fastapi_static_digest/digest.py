import json
import logging
from pathlib import Path

try:
    import jinja2
    try:
        pass_context = jinja2.pass_context
    except AttributeError:
        pass_context = jinja2.contextfunction
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fastapi_static_digest.compiler import StaticDigestCompiler
from fastapi_static_digest.settings import FastAPIStaticDigestSettings


class StaticDigest:
    pkg_settings = FastAPIStaticDigestSettings

    """Interface to cache manifest for digested static files. One of `source_dir` or 
    `static_dir` must be given.

    If `FastAPIStaticDigestSettings.RELOAD` is true, this will invoke the compilation
    step upon instantiation.

    :param source_dir: The source directory containing the static files
        that were digested. This will resolve the digested output directory
        using the default output directory specified by the StaticDigestCompiler
    :type source_dir: pathlib.Path
    :param static_dir: The output directory with the digested static files. This
        would be equivalent to the `directory` passed to fastapi.staticfiles.StaticFiles
    :type static_dir: pathlib.Path
    :raises ValueError: If neither of `source_dir` nor `static_dir` are given.
    """

    def __init__(self, source_dir=None, static_dir=None):
        if source_dir is not None:
            self.directory = StaticDigestCompiler.default_output_dir(source_dir)
        elif static_dir is not None:
            self.directory = static_dir
        else:
            raise ValueError("Must provide one of 'source_dir' or 'output_dir'")
        if self.pkg_settings.RELOAD:
            compiler = StaticDigestCompiler(source_directory=source_dir, output_dir=static_dir)
            compiler.compile()
        self.manifest_file = Path(self.directory) / "cache_manifest.json"
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        with open(self.manifest_file, "r") as f:
            return json.load(f)

    def get_digested(self, path):
        return self.manifest.get(path)

    def register_static_url_for(self, templates: Jinja2Templates):
        @pass_context
        def static_url_for(context, name, path=None) -> str:
            request: Request = context["request"]
            digested_path = self.get_digested(path)
            return request.url_for(name, path=digested_path)
        templates.env.globals['static_url_for'] = static_url_for
