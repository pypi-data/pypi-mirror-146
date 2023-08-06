__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import sys
from argparse import ArgumentParser, Namespace
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

import audioread
import magic
from audioread.exceptions import NoBackendError
from mutagen import File, MutagenError

from media_tools.util.logging import setup_logging

AUDIO_EXTENSIONS = ('mp3', 'ogg', 'flac', 'wav', 'm4a', 'aif', 'aiff')


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Print length of audio files in directories"
    )
    parser.add_argument(
        'directory', type=str, help='Directories to print'
    )
    return parser.parse_args(args)


class LengthStore:

    def __init__(self, root: Path):
        self.root = root
        self.lengths: Dict[Path, timedelta] = {}
        self.errors: Dict[Path, Exception] = {}

    def scan(self):
        self.lengths[self.root] = self.dir_length(self.root)

    @lru_cache(maxsize=100000)
    def dir_length(self, folder: Path) -> timedelta:
        length = timedelta(seconds=0)
        for thing in folder.iterdir():
            if is_audio(thing):
                length += timedelta(seconds=self.get_duration(thing))
            elif thing.is_dir():
                duration = self.dir_length(thing)
                if duration:
                    self.lengths[thing] = duration
                    length += duration
        return length

    def print(self) -> None:
        max_duration = str(self.lengths[self.root]).split('.', maxsplit=1)[0]
        for path, duration in sorted(self.lengths.items(), key=lambda item: item[1]):
            self.print_line(
                path if path == self.root else path.relative_to(self.root),
                str(duration).split('.', maxsplit=1)[0].rjust(len(max_duration))
            )

    @staticmethod
    def print_line(path: Path, duration: str) -> None:
        logging.info("%s   %s", duration, path)

    def get_duration(self, track: Path) -> float:
        try:
            audio = File(track)
            if audio:
                return audio.info.length
        except MutagenError:
            pass
        try:
            with audioread.audio_open(track) as file:
                return file.duration
        except (NoBackendError, EOFError, UnicodeEncodeError) as error:
            self.errors[track] = error
            return 0


def is_audio(track: Path):
    if not track.is_file():
        return False
    if track.suffix[1:].lower() in AUDIO_EXTENSIONS:
        return True
    file_magic = magic.from_file(str(track), mime=True)
    return file_magic.startswith('audio/')


def main() -> None:
    args: List[str] = sys.argv[1:]
    opts = parse_commandline(args)
    setup_logging(opts)
    lengths = LengthStore(Path(opts.directory))
    lengths.scan()
    lengths.print()
    if lengths.errors:
        logging.warning('%s errors', len(lengths.errors))


if __name__ == '__main__':
    main()
