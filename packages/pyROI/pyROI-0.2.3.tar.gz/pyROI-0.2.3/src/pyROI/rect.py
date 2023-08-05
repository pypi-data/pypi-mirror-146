from dataclasses import dataclass
from typing import Optional

import cv2
from numpy import ndarray

from .base import Roi
from .color import WHITE
from .color import YELLOW
from .image import Image
from .key import Key
from .point import Point
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH
from .window import named_window

__all__ = ["Rect"]


@dataclass
class Rect(Roi):
    x: int = -1
    y: int = -1
    w: int = -1
    h: int = -1
    src_size: Image = None

    def __post_init__(self) -> None:
        self._view: Optional[ndarray] = None
        self._src_raw: Optional[ndarray] = None

    @property
    def centroid(self) -> Point:
        return Point(self.x + self.w // 2, self.y + self.h // 2)

    @property
    def mask(self) -> ndarray:

        return cv2.rectangle(
            self.src_size.zero_mask,
            pt1=(self.x, self.y),
            pt2=(self.x + self.w, self.y + self.h),
            color=WHITE,
            lineType=cv2.LINE_AA,
            thickness=-1,
        )

    def select(
        self,
        src: ndarray,
        *,
        winname: str = "",
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    ) -> "Rect":
        if not isinstance(src, ndarray):
            raise TypeError("is not a numpy ndarray")

        self._start = False
        if src.ndim == 2:
            self._src_raw = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        else:
            self._src_raw = src.copy()

        self.src_size = Image(src.shape[1], src.shape[0])
        self.reset_roi()

        if not winname:
            winname = "Select region of interest (ROI)..."

        with named_window(
            winname,
            winpos_x=winpos_x,
            winpos_y=winpos_y,
            callback=self.__mouse_callback,
            hook_func=self.__post_init__,
        ) as name:
            while True:
                cv2.imshow(name, self._view)
                ret = cv2.waitKey(15) & 0xFF
                if ret in (Key.s, Key.S, Key.ENTER):
                    break
                if ret in (Key.R, Key.r):
                    self.reset_roi()
                if ret in (Key.C, Key.ESC, Key.c):
                    self.reset_roi()
                    raise KeyboardInterrupt("cancel select_area")
        return self

    def crop(self, src: ndarray) -> ndarray:
        if not isinstance(src, ndarray):
            raise TypeError("not a numpy array")

        return src[self.y : self.y + self.h, self.x : self.x + self.w]

    def reset_roi(self) -> None:
        self.x = -1
        self.y = -1
        self.w = -1
        self.h = -1
        self._start = False
        if self._src_raw is not None:
            self._view = self._src_raw.copy()

    def __mouse_callback(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_RBUTTONUP:
            self.reset_roi()

        if event == cv2.EVENT_LBUTTONDOWN:
            if (self.x, self.y) == (-1, -1) or self._start is False:
                self._view = self._src_raw.copy()
                self._start = True
                self.x = x
                self.y = y

        if event == cv2.EVENT_LBUTTONUP:
            self.w = abs(self.x - x)
            self.h = abs(self.y - y)
            self.x = min(self.x, x)
            self.y = min(self.y, y)
            self._start = False

        if self._start:
            pt1 = min(self.x, x), min(self.y, y)
            pt2 = max(self.x, x), max(self.y, y)
            self._view = cv2.rectangle(
                self._src_raw.copy(),
                pt1=pt1,
                pt2=pt2,
                color=YELLOW,
                lineType=cv2.LINE_AA,
                thickness=2,
            )
