__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from media_tools.util.logging import setup_logging
from media_tools.util.mixcloud import (
    create_mix, get_access_token, DEFAULT_CROSSFADE_MS, DEFAULT_MAX_RETRY, DEFAULT_AUDIO_FILE_TYPES
)


def parse_commandline(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        description="Creates a mix from audio files and uploads it to Mixcloud"
    )
    parser.add_argument(
        '-d', '--directory', type=str, required=True, help='Directory containing the mix'
    )
    parser.add_argument(
        '-e', '--extensions', nargs='+', default=DEFAULT_AUDIO_FILE_TYPES,
        help='List of extensions considered for the mix'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true'
    )
    parser.add_argument(
        '-s', '--strict', action='store_true', help='Fail if any required data are missing'
    )
    parser.add_argument(
        '-c', '--crossfade-ms', type=int, default=DEFAULT_CROSSFADE_MS,
        help='Milliseconds overlap between tracks'
    )
    parser.add_argument(
        '-r', '--max-retry', type=int, default=DEFAULT_MAX_RETRY,
        help='Maximum number of retries for failing uploads'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-a', '--auth-token-file', type=str, help='File containing the Mixcloud auth token'
    )
    group.add_argument(
        '-t', '--auth-token-string', type=str, help='Mixcloud auth token as string'
    )
    return parser.parse_args(args)


def main() -> None:
    args: List[str] = sys.argv[1:]
    opts = parse_commandline(args)
    setup_logging(opts)
    if opts.auth_token_string is not None:
        access_token = opts.auth_token_string
    else:
        access_token = get_access_token(Path(opts.auth_token_file))
    mix = create_mix(
        Path(opts.directory), tuple(f'?? - *.{ext}' for ext in opts.extensions), access_token,
        crossfade_ms=opts.crossfade_ms, strict=opts.strict
    )
    mix.export()
    mix.upload(max_retry=opts.max_retry)


if __name__ == '__main__':
    main()
