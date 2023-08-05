from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

from .base import Roi
from .color import RED
from .color import WHITE
from .color import YELLOW
from .image import Image
from .key import Key
from .point import calculate_distance
from .point import Point
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH
from .window import named_window

__all__ = ["Circle"]


@dataclass
class Circle(Roi):
    center: Point = None
    radius: int = 0
    src_size: Image = None

    def __post_init__(self) -> None:
        self._view: Optional[np.ndarray] = None
        self._src_raw: Optional[np.ndarray] = None
        self._run_flag = False
        self._temp: Optional[Point] = None

    @property
    def centroid(self) -> Point:
        if self.center is None:
            return Point(np.nan, np.nan)
        return self.center

    @property
    def mask(self) -> Point:
        mask = self.src_size.zero_mask
        cv2.circle(
            mask, center=self.center, radius=self.radius, color=WHITE, thickness=-1
        )
        return mask

    def select(
        self,
        src: np.ndarray,
        *,
        winname: str = "",
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    ) -> "Circle":

        self._run_flag = True
        if not isinstance(src, np.ndarray):
            raise TypeError("is not a numpy ndarray")

        if src.ndim == 2:
            self._src_raw = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        else:
            self._src_raw = src.copy()

        self.src_size = Image(src.shape[1], src.shape[0])
        self._view = self._src_raw.copy()

        if not winname:
            winname = "Select region of interest (ROI)..."

        with named_window(
            winname,
            winpos_x=winpos_x,
            winpos_y=winpos_y,
            callback=self.__mouse_callback,
        ) as name:
            while self._run_flag:
                cv2.imshow(name, self._view)
                ret = cv2.waitKey(10) & 0xFF
                if ret in (Key.ENTER, Key.S, Key.s):  # Select the roi when press
                    # show window again
                    break
        return self

    def __mouse_callback(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_LBUTTONDOWN:
            if self._temp is None:
                self._view = self._src_raw.copy()
                self.center = None
                self.radius = 0
                self._temp = Point(x, y)

        if event == cv2.EVENT_LBUTTONUP:
            self.center = Point._make(self._temp)
            self.radius = calculate_distance(self._temp, Point(x, y))
            self._temp = None

        if event == cv2.EVENT_RBUTTONUP:
            self._temp = None
            self._run_flag = False

        if self.radius:
            self.update_image(self.center, self.radius)
        else:
            center = self._temp
            if center is None:
                center = Point(x, y)
            self.update_image(center, calculate_distance(center, Point(x, y)))

    def update_image(self, center: Point, radius: int) -> None:
        _mask = np.zeros_like(self._src_raw, dtype=np.uint8)
        cv2.circle(_mask, center=center, radius=radius, color=YELLOW, thickness=-1)
        cv2.circle(_mask, center=center, radius=2, color=RED, thickness=-1)
        self._view = cv2.addWeighted(
            src1=self._src_raw,
            alpha=1,
            src2=_mask,
            beta=0.75,
            gamma=0,
        )
