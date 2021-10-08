# fastapi_static_digest package

## Submodules

## Module contents


### class fastapi_static_digest.StaticDigest(source_dir=None, static_dir=None)
Bases: `object`

Interface to cache manifest for digested static files. One of source_dir or 
static_dir must be given.


* **Parameters**

    
    * **source_dir** (*pathlib.Path*) – The source directory containing the static files
    that were digested. This will resolve the digested output directory
    using the default output directory specified by the StaticDigestCompiler


    * **static_dir** (*pathlib.Path*) – The output directory with the digested static files. This
    would be equivalent to the directory passed to fastapi.staticfiles.StaticFiles



* **Raises**

    **ValueError** – If neither of source_dir nor static_dir are given.



#### get_digested(path)

#### register_static_url_for(templates: starlette.templating.Jinja2Templates)

### class fastapi_static_digest.StaticDigestCompiler(source_directory: pathlib.Path, output_dir: Optional[pathlib.Path] = None, gzip: bool = False)
Bases: `object`

Tags and optionally compresses (gzip) files in the source_directory.
NOTE: The clean method will remove the output_dir

It will attempt to copy the original file permissions, and will log a warning 
if it fails to do so.


* **Parameters**

    
    * **source_directory** (pathlib.Path) – The source directory containing the static files
    to be digested. Must be a Path object. String paths are not supported.


    * **output_dir** (Optional[pathlib.Path]) – An optional output directory where the digested files
    will be written. This will default to a “_digest/” directory under the
    source_directory. If the output_dir is used for other purposes, please be
    warned that invoking the clean method will remove this directory.


    * **gzip** (bool) – A boolean indicating whether or not to _additionally_ include
    gzipped copies of the files in the output_dir.



#### DEFAULT_OUTPUT_DIR( = './_digest')

#### clean()

#### compile()

#### classmethod default_output_dir(source_dir)
