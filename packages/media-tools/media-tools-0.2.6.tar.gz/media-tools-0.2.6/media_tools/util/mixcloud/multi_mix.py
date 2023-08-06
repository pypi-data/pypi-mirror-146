__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
from math import ceil
from pathlib import Path
from typing import List

from media_tools.util.mixcloud.mix import Mix
from media_tools.util.mixcloud.constants import (
    DEFAULT_CROSSFADE_MS, MIXCLOUD_MAX_FILESIZE, DEFAULT_MAX_RETRY, MP3_KBIT_RATE
)


def bytes_per_second(mp3_kbit_rate: int = MP3_KBIT_RATE) -> int:
    return mp3_kbit_rate // 8 * 1024 * 2


# noinspection PyMissingConstructor
class MultiMix(Mix):

    def __init__(  # pylint: disable=super-init-not-called, too-many-arguments
            self, basedir: Path, files: List[str], access_token: str, total_length: int,
            strict: bool = False, crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
    ) -> None:
        self._basedir = basedir
        self._title = title
        self._incomplete = False
        self._mix_parts: List[Mix] = []
        self._part_paths: List[Path] = []
        oversize_factor = ceil(total_length * bytes_per_second() / MIXCLOUD_MAX_FILESIZE)
        chunk_size = len(files) // oversize_factor
        for i in range(oversize_factor):
            part_files = tuple(files[i * chunk_size:(i + 1) * chunk_size])
            part_name = f"{self.title} Part {i + 1}"
            logging.info(part_name)
            mix_part = Mix(
                basedir, part_files, access_token,
                strict=strict, crossfade_ms=crossfade_ms, title=part_name
            )
            self._mix_parts.append(mix_part)

    @property
    def parts(self):
        return self._mix_parts

    def upload(self, name: Path = Path('mix.mp3'), max_retry: int = DEFAULT_MAX_RETRY) -> None:
        for mix_part, part_path in zip(self._mix_parts, self._part_paths):
            mix_part.upload(part_path, max_retry)

    def export(self, name: Path = Path('mix.mp3')) -> None:
        for i, mix_part in enumerate(self._mix_parts):
            part_path = Path(f"{name.stem}_{i + 1}{name.suffix}")
            mix_part.export(part_path)
            self._part_paths.append(part_path)
