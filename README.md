# FastAPI Static Digest

A Starlette/FastAPI plugin to digest and compress static files, and integrate with Jinja templates.

`pip install fastapi-static-digest`

# Overview

There are two classes: StaticDigest and StaticDigestCompiler.

The `StaticDigestCompiler.compiler` method will produce the digested directory. The `StaticDigest` (and `starlette.staticfiles.StaticFiles`) should be configured to read this directory. 

The compilation can be added to your build process, for instance with a `click` CLI command (see below). Alternatively, the `FASTAPI_STATICDIGEST_RELOAD=1` environment variable can be set to enable "hot reloading" during development.

# Usage

```python
# app.py

app_root = Path(__file__).parent
static_src =  app_root / "static"
static = StaticDigest(source_dir=static_src)

routes = [
    Mount('/static', app=StaticFiles(directory=static.directory), name="static"),
]

app = Starlette(routes=routes)
```

```python
# manage.py

from .app import app_root


@click.command()
def compile():
    src = app_root / "static"
    click.echo("Source dir %s" % src)
    compiler = StaticDigestCompiler(source_directory=src)
    compiler.compile()
    click.echo("Done.")
```

## Jinja2 Integration

```python
# app.py

app_root = Path(__file__).parent
static_src =  app_root / "static"
static = StaticDigest(source_dir=static_src)
templates = Jinja2Templates(app_root / "templates")
static.register_static_url_for(templates)

routes = [
    Mount('/static', app=StaticFiles(directory=static.directory), name="static"),
]

app = Starlette(routes=routes)
```

```html
<!-- index.html -->
{{ static_url_for("static", "app.css" )}}
```

renders to 

```html
https://myhost.com/static/app.92fede82119d2e012f890e1102080a45.css
```

# Development

PRs and issues are welcome! 