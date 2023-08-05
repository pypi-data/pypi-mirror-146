import math
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

from .base import Roi
from .color import BLACK
from .color import GREEN
from .color import RED
from .color import WHITE
from .color import YELLOW
from .image import Image
from .key import Key
from .point import calculate_distance
from .point import Point
from .point import Vector2D
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH
from .window import named_window

__all__ = ["Ellipse"]


@dataclass
class Ellipse(Roi):
    center: Point = None
    major_axis: Vector2D = None
    minor_axis: Vector2D = None
    axis_ratio: float = 0.6
    src_size: Image = None

    def __post_init__(self) -> None:
        self._view: Optional[np.ndarray] = None
        self._src_raw: Optional[np.ndarray] = None
        self._run_flag = False
        self._temp: Optional[Point] = None
        if not isinstance(self.major_axis, (Vector2D, type(None))):
            raise TypeError("major_axis is not Vector2D")

        if isinstance(self.minor_axis, Vector2D):
            self.axis_ratio = self.minor_axis.length / self.major_axis.length
        else:
            self.minor_axis = self.get_minor_axis(self.major_axis)

    def get_minor_axis(self, major_axis: Optional[Vector2D]) -> Optional[Vector2D]:
        if major_axis is None:
            return None
        i = major_axis.j * self.axis_ratio
        j = major_axis.i * self.axis_ratio * (-1)
        return Vector2D(int(i), int(j))

    @property
    def centroid(self) -> Point:
        if self.center is None:
            return Point(np.nan, np.nan)
        return self.center

    @property
    def mask(self) -> Point:
        return cv2.ellipse(
            self.src_size.zero_mask,
            self.center,
            axes=(int(self.major_axis.length), int(self.minor_axis.length)),
            angle=int(self.major_axis.angle / math.pi * 180),
            startAngle=0,
            endAngle=360,
            color=WHITE,
            thickness=-1,
        )

    def select(
        self,
        src: np.ndarray,
        *,
        winname: str = "",
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    ) -> "Ellipse":

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
        print("Press `w` or `s` to adjust the ratio of ellipse axes")
        with named_window(
            winname,
            winpos_x=winpos_x,
            winpos_y=winpos_y,
            callback=self.__mouse_callback,
        ) as name:
            while self._run_flag:
                cv2.imshow(name, self._view)
                ret = cv2.waitKey(10) & 0xFF
                if ret in (
                    Key.ENTER,
                    Key.ESC,
                    Key.Q,
                    Key.q,
                ):
                    break
                if ret in (Key.S, Key.s, Key.W, Key.w):
                    if ret in (Key.W, Key.w):
                        self.axis_ratio += 0.025
                    if ret in (Key.S, Key.s):
                        self.axis_ratio -= 0.025
                    self.minor_axis = self.get_minor_axis(self.major_axis)
                    self.update_image(self.center, self.major_axis, self.minor_axis)

        return self

    def __mouse_callback(self, event, x, y, flags, param) -> None:

        curr = Point(x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            if self._temp is None:
                self._view = self._src_raw.copy()
                self.center = None
                self.major_axis = None
                self.minor_axis = None
                self._temp = curr

        major_axis = Vector2D.from_points(self._temp or self.center or curr, curr)
        minor_axis = self.get_minor_axis(major_axis)

        if event == cv2.EVENT_LBUTTONUP:
            self.center = Point._make(self._temp)
            self.major_axis = Vector2D.from_points(
                self._temp or self.center or curr, curr
            )
            self.minor_axis = self.get_minor_axis(self.major_axis)
            self._temp = None

        if event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                self.axis_ratio += 0.025
            else:
                self.axis_ratio -= 0.025
            minor_axis = self.get_minor_axis(major_axis)
            self.minor_axis = minor_axis

        if event == cv2.EVENT_RBUTTONUP:
            self._temp = None
            self._run_flag = False

        center = self._temp or self.center or curr
        if self.major_axis:
            major_axis = self.major_axis

        minor_axis = self.get_minor_axis(major_axis)
        self.update_image(center, major_axis, minor_axis)

    def update_image(
        self, center: Point, major_axis: Vector2D, minor_axis: Vector2D
    ) -> None:
        _mask = np.zeros_like(self._src_raw, dtype=np.uint8)
        print(major_axis.angle, major_axis.angle * math.pi, major_axis.angle / math.pi)

        _mask = cv2.ellipse(
            _mask,
            center,
            axes=(int(major_axis.length), int(minor_axis.length)),
            angle=int(major_axis.angle / math.pi * 180),
            startAngle=0,
            endAngle=360,
            color=YELLOW,
            thickness=-1,
        )

        pt2 = Point(center.x + major_axis.i, center.y + major_axis.j)
        _mask = cv2.line(_mask, center, pt2, color=RED, thickness=2)
        cv2.circle(_mask, center=pt2, radius=3, color=GREEN, thickness=-1)

        pt2 = Point(max(0, center.x + minor_axis.i), max(0, center.y + minor_axis.j))
        _mask = cv2.line(_mask, center, pt2, color=GREEN, thickness=2)

        cv2.circle(_mask, center=center, radius=3, color=RED, thickness=-1)
        self._view = cv2.addWeighted(
            src1=self._src_raw,
            alpha=1,
            src2=_mask,
            beta=0.75,
            gamma=0,
        )
