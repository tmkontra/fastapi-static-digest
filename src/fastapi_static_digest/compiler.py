import gzip
import hashlib
import json
import logging
from pathlib import Path
import os
import shutil
from typing import List, Mapping, Optional


logger = logging.getLogger(__name__)


class StaticDigestCompiler:
    """Tags and optionally compresses (gzip) files in the `source_directory`.
    NOTE: The `clean` method will remove the `output_dir`

    It will attempt to copy the original file permissions, and will log a warning 
    if it fails to do so.

    :param source_directory: The source directory containing the static files
        to be digested. Must be a Path object. String paths are not supported.
    :type source_directory: `pathlib.Path`
    :param output_dir: An optional output directory where the digested files
        will be written. This will default to a "_digest/" directory under the
        `source_directory`. If the `output_dir` is used for other purposes, please be
        warned that invoking the `clean` method will remove this directory.
    :type output_dir: `Optional[pathlib.Path]`
    :param gzip: A boolean indicating whether or not to _additionally_ include
        gzipped copies of the files in the output_dir.
    :type gzip: `bool`
    """

    DEFAULT_OUTPUT_DIR = "./_digest"

    def __init__(self, source_directory: Path, output_dir: Optional[Path] = None, gzip: bool = False):
        self.source_directory = source_directory
        self.output_directory = output_dir or self.default_output_dir(self.source_directory)
        self.manifest_file = Path(self.output_directory) / "cache_manifest.json"
        self.gzip = gzip
        self._warned = False

    def compile(self):    
        self._make_output_dir()
        files = self._list_files()
        manifest = self._manifest(files)
        self._copy_files(manifest)
        with open(self.manifest_file, "w") as f:
            json.dump(manifest, f)
            
    def clean(self):
        if self.output_directory.exists():
            shutil.rmtree(self.output_directory)

    @classmethod
    def default_output_dir(cls, source_dir) -> Path:
        return Path(source_dir) / cls.DEFAULT_OUTPUT_DIR

    def _list_files(self):
        input_files = []
        for (dirpath, _, filenames) in os.walk(self.source_directory):
            # if output is subdir of source, skip
            if Path(dirpath).is_relative_to(self.output_directory):
                continue
            for filename in filenames:
                p = Path(dirpath) / filename
                input_files.append(p)
        return input_files

    def _manifest(self, input_files: List[Path]):
        manifest = {}
        rel_out = self.source_directory.relative_to(self.source_directory)
        for abspath in input_files:
            digest = self._digest(abspath)
            filename = abspath.stem
            file_ext = abspath.suffix
            output_filename = f"{filename}.{digest}{file_ext}"
            relpath = abspath.relative_to(self.source_directory)
            outpath = rel_out / relpath.with_name(output_filename)
            manifest[str(relpath)] = str(outpath)
        return manifest
        
    @staticmethod
    def _digest(file):
        digest = None
        with open(file, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
        return digest
    
    def _copy_files(self, manifest: Mapping[Path, Path]):
        for input_path, output_path in manifest.items():
            input_path = self.source_directory / input_path
            output_path = self.output_directory / output_path
            if not output_path.parent.exists():
                output_path.parent.mkdir(exist_ok=True)
            self._copy(input_path, output_path)
            if self.gzip:
                self._copy_gzip(input_path, output_path)

    def _copy(self, input, output):
        shutil.copy2(input, output)

    def _copy_gzip(self, input: Path, output: Path):
        gz_file = output.parent / f"{output}.gz"
        with open(input, "rb") as original:
            with gzip.open(gz_file, "wb") as gzipped:
                shutil.copyfileobj(original, gzipped)
        try:
            shutil.copystat(input, gz_file)
        except NotImplementedError:
            if not self._warned:
                logger.warn("Unable to copy file metadata!")
                self._warned = True

    def _make_output_dir(self):
        self.output_directory.mkdir(exist_ok=True)
