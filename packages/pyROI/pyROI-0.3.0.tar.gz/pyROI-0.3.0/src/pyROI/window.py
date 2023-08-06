import os
import uuid
from typing import Callable

import cv2
from numpy import ndarray

from .key import Key
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH

cv2.setNumThreads(os.cpu_count())

__all__ = ["NamedWindow", "show_window"]

USED_WINNAME = set()


def verify_winname(winname: str) -> str:
    name = winname
    while name in USED_WINNAME:
        name = f"{winname}-{uuid.uuid1().hex[:8]}"
    USED_WINNAME.add(name)
    return name


class NamedWindow:
    USED_WINNAME = set()

    def __init__(
        self,
        winname: str,
        *,
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
        callback: Callable = None,
        hook_func: Callable = None,
    ):
        self.name = self.verify_winname(winname)
        self.winpos_x = winpos_x
        self.winpos_y = winpos_y
        self.callback = callback
        self.hook_func = hook_func

    def __enter__(self) -> "NamedWindow":
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.name, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        cv2.setWindowProperty(self.name, cv2.WND_PROP_TOPMOST, 0)
        cv2.moveWindow(self.name, self.winpos_x, self.winpos_y)
        if callable(self.callback):
            cv2.setMouseCallback(self.name, self.callback)
        cv2.startWindowThread()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_window(self.name)
        if callable(self.hook_func):
            self.hook_func()

    def imshow(self, image: ndarray) -> "NamedWindow":
        cv2.imshow(self.name, image)
        return self

    def waitKey(self, milliseconds: int) -> int:
        return cv2.waitKey(milliseconds) & 0xFF

    def getWindowProperty(self, CV_WND_PROP):
        return cv2.getWindowProperty(self.name, CV_WND_PROP)

    @classmethod
    def verify_winname(cls, winname: str) -> str:
        name = winname
        while name in cls.USED_WINNAME:
            name = f"{winname}-{uuid.uuid1().hex[:8]}"
        cls.USED_WINNAME.add(name)
        return name

    @classmethod
    def close_window(cls, winname: str) -> None:
        try:
            cv2.waitKey(1)
            cv2.destroyWindow(winname)
            if winname in cls.USED_WINNAME:
                cls.USED_WINNAME.remove(winname)
            cv2.waitKey(1)
        except cv2.error as e:
            if e.code != -27:
                raise e


def show_window(src: ndarray, *, winname: str = "", **kwargs):
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

    with NamedWindow(winname, **kwargs) as win:
        while True:
            ret = win.imshow(src).waitKey(15)
            if ret in (Key.ESC, Key.ENTER, Key.Q, Key.q):
                break
            if win.getWindowProperty(cv2.WND_PROP_VISIBLE) < 1:
                break
