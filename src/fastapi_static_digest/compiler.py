import hashlib
import json
from pathlib import Path
import os
import shutil
from typing import List, Mapping, Union


class StaticDigestCompiler:
    DEFAULT_OUTPUT_DIR = "../static_digest"

    def __init__(self, source_directory, output_dir=None, gzip=False):
        self.source_directory = source_directory
        self.output_directory = output_dir or self.default_output_dir(self.source_directory)
        self.manifest_file = Path(self.output_directory) / "cache_manifest.json"
        self.gzip = gzip

    @classmethod
    def default_output_dir(cls, source_dir):
        return Path(source_dir) / cls.DEFAULT_OUTPUT_DIR

    def _list_files(self):
        input_files = []
        for (dirpath, _, filenames) in os.walk(self.source_directory):
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

    def _copy_gzip(self, input, output):
        pass

    def _copy(self, input, output):
        shutil.copy2(input, output)
    
    def _copy_files(self, manifest: Mapping[Path, Path]):
        for input_path, output_path in manifest.items():
            input_path = self.source_directory / input_path
            output_path = self.output_directory / output_path
            if not output_path.parent.exists():
                output_path.parent.mkdir(exist_ok=True)
            if self.gzip:
                self._copy_gzip(input_path, output_path)
            else:
                self._copy(input_path, output_path)

    def clean(self):
        if self.output_directory.exists():
            shutil.rmtree(self.output_directory)

    def _make_output_dir(self):
        self.output_directory.mkdir(exist_ok=False)

    def compile(self):
        self.clean()    
        self._make_output_dir()
        files = self._list_files()
        manifest = self._manifest(files)
        self._copy_files(manifest)
        with open(self.manifest_file, "w") as f:
            json.dump(manifest, f)
    