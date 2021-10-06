import gzip
import hashlib
import json
import logging
from pathlib import Path
import os
import shutil
from typing import List, Mapping
import typing


logger = logging.getLogger(__name__)


class StaticDigestCompiler:
    """

    :param client: A handle to the :class:`simpleble.SimpleBleClient` client
        object that detected the device
    :type client: class:`simpleble.SimpleBleClient`
    :param addr: Device MAC address, defaults to None
    :type addr: str, optional
    :param addrType: Device address type - one of ADDR_TYPE_PUBLIC or
        ADDR_TYPE_RANDOM, defaults to ADDR_TYPE_PUBLIC
    :type addrType: str, optional
    :param iface: Bluetooth interface number (0 = /dev/hci0) used for the
        connection, defaults to 0
    :type iface: int, optional
    :param data: A list of tuples (adtype, description, value) containing the
        AD type code, human-readable description and value for all available
        advertising data items, defaults to None
    :type data: list, optional
    :param rssi: Received Signal Strength Indication for the last received
        broadcast from the device. This is an integer value measured in dB,
        where 0 dB is the maximum (theoretical) signal strength, and more
        negative numbers indicate a weaker signal, defaults to 0
    :type rssi: int, optional
    :param connectable: `True` if the device supports connections, and `False`
        otherwise (typically used for advertising ‘beacons’).,
        defaults to `False`
    :type connectable: bool, optional
    :param updateCount: Integer count of the number of advertising packets
        received from the device so far, defaults to 0
    :type updateCount: int, optional
    """

    DEFAULT_OUTPUT_DIR = "./_digest"

    def __init__(self, source_directory, output_dir=None, gzip=False):
        self.source_directory = source_directory
        self.output_directory = output_dir or self.default_output_dir(self.source_directory)
        self.manifest_file = Path(self.output_directory) / "cache_manifest.json"
        self.gzip = gzip
        self._warned = False

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

    def _copy(self, input, output):
        shutil.copy2(input, output)
    
    def _copy_files(self, manifest: Mapping[Path, Path]):
        for input_path, output_path in manifest.items():
            input_path = self.source_directory / input_path
            output_path = self.output_directory / output_path
            if not output_path.parent.exists():
                output_path.parent.mkdir(exist_ok=True)
            self._copy(input_path, output_path)
            if self.gzip:
                self._copy_gzip(input_path, output_path)

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
    