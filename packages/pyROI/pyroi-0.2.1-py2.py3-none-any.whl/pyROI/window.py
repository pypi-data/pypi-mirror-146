import os
import uuid
from contextlib import contextmanager
from typing import Callable

import cv2
from numpy import ndarray

from .key import Key
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH

cv2.setNumThreads(os.cpu_count())

__all__ = ["named_window", "show_window"]

USED_WINNAME = set()


def verify_winname(winname: str) -> str:
    name = winname
    while name in USED_WINNAME:
        name = f"{winname}-{uuid.uuid1().hex[:8]}"
    USED_WINNAME.add(name)
    return name


def close_window(winname: str) -> None:
    cv2.waitKey(1)
    cv2.destroyWindow(winname)
    USED_WINNAME.remove(winname)
    cv2.waitKey(1)


@contextmanager
def named_window(
    winname: str,
    *,
    winpos_x: int = SCREEN_WIDTH // 2 - 100,
    winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    callback: Callable = None,
    hook_func: Callable = None,
):
    try:
        name = verify_winname(winname)
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(name, winpos_x, winpos_y)
        if callable(callback):
            cv2.setMouseCallback(name, callback)
        cv2.startWindowThread()
        yield name
    finally:
        close_window(name)
        if callable(hook_func):
            hook_func()


def show_window(src: ndarray, *, winname: str = ""):
    """Display source image using opencv

    Args:
        src (ndarray): source image to show
        winname (str, optional): window title. Defaults to "".

    Raises:
        TypeError: _description_
    """
    if not isinstance(src, ndarray):
        raise TypeError("src is not ndarray")
    if not winname:
        winname = "image"

    with named_window(winname):
        while True:
            cv2.imshow(winname, src)
            ret = cv2.waitKey(15) & 0xFF
            if ret in (Key.ESC, Key.ENTER, Key.Q, Key.q):
                break
