import pathlib
import struct
import subprocess as sp
import sys


def retrieve() -> tuple[int, int]:
    home = pathlib.Path(__file__).resolve().parent
    runner = home.joinpath("__runner__.py")
    cache_file = home.joinpath("__pycache__", "__cache__")
    width, height = 1200, 800
    try:
        if not cache_file.is_file():
            proc = sp.Popen(
                [sys.executable, str(runner).encode()],
                stdin=sp.PIPE,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
            )
            proc.communicate()
        recv = cache_file.read_bytes()
        width, height = struct.unpack("<ll", recv)
    except Exception as e:
        print(e)
    if not isinstance(width) or width <= 0:
        width = 1280
    if not isinstance(height) or height <= 0:
        height = 800
    return width, height


SCREEN_WIDTH, SCREEN_HEIGHT = retrieve()

__all__ = ["SCREEN_WIDTH", "SCREEN_HEIGHT"]
