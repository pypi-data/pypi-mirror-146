__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
import re
import sys
from pathlib import Path
from time import sleep
from typing import Tuple, List, Dict, Optional

import requests
from pydub import AudioSegment
from tinytag import TinyTag

from media_tools.util.mixcloud.constants import (
    DEFAULT_CROSSFADE_MS, DEFAULT_MAX_RETRY, MP3_KBIT_RATE, MIXCLOUD_API_UPLOAD_URL
)


class Mix:  # pylint: disable=too-many-instance-attributes

    @classmethod
    def scan(cls, basedir: Path, patterns: Tuple[str, ...]) -> Tuple[List[str], int]:
        audio_files = sorted([f for p in patterns for f in basedir.glob(p)])
        length = sum([TinyTag.get(str(audio_file)).duration for audio_file in audio_files])
        return [f.name for f in audio_files], int(length)

    def __init__(  # pylint: disable=too-many-arguments
            self, basedir: Path, patterns: Tuple[str, ...], access_token: str,
            strict: bool = False, crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
    ) -> None:
        self._basedir = basedir
        self._strict = strict
        self._crossfade_ms = crossfade_ms
        self._title = title
        self._incomplete = False
        self._track_info: List[Dict] = []
        self._access_token = access_token
        audio_files = sorted([f for p in patterns for f in self._basedir.glob(p)])
        self._audio = self._import_audio(audio_files)

    @property
    def valid(self):
        return not self._incomplete

    @property
    def tags(self) -> List[str]:
        if (self._basedir / 'tags.txt').exists():
            with (self._basedir / 'tags.txt').open() as file:
                tags = list(line for line in (line.strip() for line in file) if line)
            if len(tags) <= 5:
                return tags
            self._incomplete = True
            raise ValueError(f'Max. 5 tags allowed, found {len(tags)}: {tags}')
        self._incomplete = True
        if self._strict:
            raise ValueError('No tags found')
        logging.warning('No tags found')
        return ['Testing Mixcloud API']

    @property
    def title(self) -> str:
        if self._title:
            return self._title
        title = re.sub(r'^\d+ - ', '', self._basedir.resolve().name)
        return f"Test - don't bother playing ({title})" if self._incomplete else title

    @property
    def description(self) -> str:
        if (self._basedir / 'description.txt').exists():
            with (self._basedir / 'description.txt').open() as file:
                return file.read().strip()
        if self._strict:
            raise ValueError('No description found')
        logging.warning('No description found')
        self._incomplete = True
        return 'Test test test'

    @property
    def picture(self) -> Optional[Path]:
        """Currently just returns the first JPEG or PNG. Room for improvement!"""
        try:
            return next(self._basedir.glob('*.*p*g'))
        except StopIteration as error:
            if self._strict:
                raise ValueError(f"No picture in {self._basedir}") from error
            logging.warning('No picture found')
            self._incomplete = True
            return None

    def _import_audio(self, audio_files: List[Path]) -> AudioSegment:
        audio = AudioSegment.empty()
        for i, audio_file in enumerate(audio_files):
            self._track_info.append(self._get_track_info(audio_file))
            logging.info("%s - %s", i + 1, audio_file.name)
            track = AudioSegment.from_file(audio_file)
            track = track.normalize()
            audio = audio.append(
                track,
                crossfade=self._crossfade_ms if len(audio) > self._crossfade_ms else len(audio)
            )

        return audio

    def _get_track_info(self, audio_file: Path) -> Dict:
        tags = TinyTag.get(str(audio_file))
        if tags.artist is None or tags.title is None:
            if self._strict:
                raise ValueError(f"Incomplete tags for {audio_file}")
            logging.warning("Incomplete tags for %s", audio_file)
            self._incomplete = True
            return {
                'artist': tags.artist or '???', 'title': tags.title or '???',
                'length': tags.duration
            }
        return {
            'artist': tags.artist, 'title': tags.title, 'length': tags.duration,
            'filename': audio_file.name
        }

    def export(self, name: Path = Path('mix.mp3')) -> None:
        mix_file = self._basedir / name
        audio_format = name.suffix[1:]
        logging.info('Exporting to %s with bitrate %s kbps', mix_file, MP3_KBIT_RATE)
        self._audio.export(
            mix_file, format=audio_format, parameters=["-q:a", "0"], bitrate=f'{MP3_KBIT_RATE}k'
        )

    def upload(self, name: Path = Path('mix.mp3'), max_retry: int = DEFAULT_MAX_RETRY) -> None:
        url = MIXCLOUD_API_UPLOAD_URL + '/?access_token=' + self._access_token
        mix_file = self._basedir / name
        if not mix_file.exists():
            raise FileNotFoundError(mix_file)
        files = {
            'mp3': ('mix.mp3', mix_file.open('rb'), 'audio/mpeg'),
        }
        if self.picture:
            picture_type = self.picture.suffix
            files['picture'] = (
                'picture' + picture_type, self.picture.open('rb'),
                f'image/{"png" if picture_type == ".png" else "jpeg"}'
            )

        data = {
            'name': self.title,
            'description': self.description,
            'percentage_music': 100
        }
        self._add_tags(data)
        self._add_track_info(data)
        size_bytes = mix_file.stat().st_size + self.picture.stat().st_size if self.picture else 0
        logging.info(
            'Uploading %s kBytes (%s minutes) as %s',
            f'{size_bytes // 1024:,d}',
            f'{len(self._audio) // 60000}:{len(self._audio) % 60000 // 1000:02}',
            self.title
        )

        try:
            response = requests.post(url, files=files, data=data)
        except requests.exceptions.ConnectionError as error:
            logging.warning(self.connection_error_message(error, max_retry))
            if max_retry > 0:
                self.upload(name, max_retry=max_retry - 1)
                return
            sys.exit(1)
        else:
            logging.info(self.response_message(response))
            if self.is_rate_limited(response) and max_retry > 0:
                sleep(int(response.json()['error']['retry_after']))
                self.upload(name, max_retry=max_retry - 1)
            else:
                sys.exit(1)

    @staticmethod
    def is_rate_limited(response: requests.Response) -> bool:
        return response.status_code == 403 and \
            response.json().get('error', {}).get('type') == 'RateLimitException'

    @staticmethod
    def response_message(response: requests.Response) -> str:
        if response.status_code == 200:
            return f"{response.status_code}: {response.json()['result']['message']}"
        return f"{response.status_code}: {response.json()['error']}"

    @staticmethod
    def connection_error_message(error: requests.exceptions.ConnectionError, max_retry: int) -> str:
        message = ""
        if error.args:
            message = f"{error.args[0].args[1].args[1]}: {error.args[0].args[0]} "
        if max_retry > 0:
            message += f"Retrying {max_retry} time{'s' if max_retry > 1 else ''}."
        else:
            message += "Giving up."
        return message

    def _add_tags(self, data: Dict) -> None:
        for i, tag in enumerate(self.tags):
            data[f"tags-{i}-tag"] = tag

    def _add_track_info(self, data: Dict) -> None:
        start_time = 0
        for i, track_info in enumerate(self._track_info):
            data[f"sections-{i}-artist"] = track_info['artist']
            data[f"sections-{i}-song"] = track_info['title']
            data[f"sections-{i}-start_time"] = int(start_time)
            start_time += (track_info['length'] - self._crossfade_ms / 1000)
