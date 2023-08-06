__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from pathlib import Path
from typing import Tuple, Optional

from .authorization_error import AuthorizationError
from .constants import (
    MP3_KBIT_RATE, DEFAULT_CROSSFADE_MS, MIXCLOUD_MAX_FILESIZE, ACCESS_TOKEN_FILE,
    ACCESS_TOKEN_SEARCH_PATH
)
from .mix import Mix
from .multi_mix import MultiMix


def bytes_per_second(mp3_kbit_rate: int = MP3_KBIT_RATE) -> int:
    return mp3_kbit_rate // 8 * 1024 * 2


def create_mix(  # pylint: disable=too-many-arguments
        basedir: Path, patterns: Tuple[str, ...], access_token: str,
        strict: bool = False, crossfade_ms: int = DEFAULT_CROSSFADE_MS, title: str = None
) -> "Mix":
    files, length = Mix.scan(basedir, patterns)
    if bytes_per_second() * length < MIXCLOUD_MAX_FILESIZE:
        return Mix(basedir, patterns, access_token, strict, crossfade_ms, title)
    return MultiMix(
        basedir, files, access_token, length, strict, crossfade_ms, title
    )


def get_access_token(access_token_path: Optional[Path] = None) -> str:
    error_message = f"""
Authorization token does not exist - please follow the instructions at
https://www.mixcloud.com/developers/#authorization to generate an auth
token and store it under ./{ACCESS_TOKEN_FILE}, ~/{ACCESS_TOKEN_FILE}
or ~/.config/{ACCESS_TOKEN_FILE}.
"""
    if not access_token_path:
        for basedir in ACCESS_TOKEN_SEARCH_PATH:
            if (basedir / ACCESS_TOKEN_FILE).exists():
                access_token_path = basedir / ACCESS_TOKEN_FILE
                break
    if access_token_path is None:
        raise AuthorizationError(error_message)
    try:
        with access_token_path.open('r') as file:
            return file.read().strip()
    except OSError as error:
        raise AuthorizationError(error_message) from error
