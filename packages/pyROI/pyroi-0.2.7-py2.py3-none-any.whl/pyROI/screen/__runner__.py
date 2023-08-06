import struct
import tkinter
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def tk_instance():
    root = tkinter.Tk()
    root.wm_withdraw()
    yield root
    root.destroy()


def retrieve_screen_resolution() -> tuple[int, int]:
    with tk_instance() as root:
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
    return width, height


def runner():
    folder = Path(__file__).resolve().parent / "__pycache__"
    cache_file = folder / "__cache__"
    if not folder.is_dir():
        folder.mkdir()
    if cache_file.exists():
        return
    width, height = retrieve_screen_resolution()
    with open(cache_file, "wb") as f:
        f.write(struct.pack("<ll", width, height))


if __name__ == "__main__":
    runner()
