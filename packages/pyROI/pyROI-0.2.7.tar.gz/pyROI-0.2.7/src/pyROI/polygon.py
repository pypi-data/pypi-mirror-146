from contextlib import ExitStack
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

from .base import Roi
from .color import BLUE
from .color import RED
from .color import WHITE
from .color import YELLOW
from .image import Image
from .key import Key
from .point import Point
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH
from .window import named_window

__all__ = ["Polygon"]


@dataclass
class Polygon(Roi):
    verts: list[Point] = field(init=False, default_factory=list)
    src_size: Image = None

    def __post_init__(self) -> None:
        self._view: Optional[ndarray] = None
        self._src_raw: Optional[ndarray] = None
        self._run_flag: bool = False

    @property
    def points(self) -> ndarray:
        return np.array(self.verts, dtype=np.int32)

    @property
    def centroid(self) -> Point:
        if not self.verts:
            return Point(np.nan, np.nan)
        centroid_f = self.points.astype(float).mean(axis=0)
        return Point._make(np.round(centroid_f).astype(int))

    @property
    def mask(self) -> np.ndarray:
        return cv2.fillPoly(self.src_size.zero_mask, pts=[self.points], color=WHITE)

    def select(
        self,
        src: ndarray,
        *,
        winname: str = "",
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    ) -> "Polygon":

        self.verts.clear()
        self._run_flag = True
        if not isinstance(src, ndarray):
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

        mask = np.zeros_like(self._src_raw, dtype=np.uint8)
        if self.verts:
            cv2.fillPoly(mask, [self.points], YELLOW)

        overlap = cv2.addWeighted(
            src1=self._src_raw,
            alpha=0.75,
            src2=mask,
            beta=0.25,
            gamma=0,
        )
        shift = src.shape[1] // 2
        with ExitStack() as stack:
            mask_winname = stack.enter_context(
                named_window(
                    "mask",
                    winpos_x=max(winpos_x - shift, 0),
                    winpos_y=winpos_y,
                    hook_func=cv2.destroyAllWindows,
                )
            )
            overlap_winname = stack.enter_context(
                named_window(
                    "overlap",
                    winpos_x=max(winpos_x + shift, 0),
                    winpos_y=winpos_y,
                    hook_func=cv2.destroyAllWindows,
                )
            )
            stack.callback(self.__post_init__)
            checked = False
            while not checked:
                cv2.imshow(mask_winname, mask)
                cv2.imshow(overlap_winname, overlap)
                ret = cv2.waitKey(10) & 0xFF
                if ret in (Key.R, Key.r):
                    break
                if ret in (Key.ENTER, Key.s, Key.S):
                    checked = True

        if not checked:
            # re-select
            return self.select(
                src,
                winname=winname,
                winpos_x=winpos_x,
                winpos_y=winpos_y,
            )

        return self

    def __mouse_callback(self, event, x, y, flags, param) -> None:

        if event == cv2.EVENT_LBUTTONUP:
            self.verts.append(Point(x, y))

        if event == cv2.EVENT_RBUTTONDOWN:
            if len(self.verts):
                self.verts.pop()

        if event == cv2.EVENT_MBUTTONDOWN:
            self._run_flag = False

        if self.verts:
            self.update_image()

    def update_image(self) -> None:
        _mask = np.zeros_like(self._src_raw, dtype=np.uint8)
        _mask = cv2.fillPoly(_mask, pts=[self.points], color=YELLOW)
        _mask = cv2.polylines(
            _mask,
            [self.points],
            isClosed=True,
            color=BLUE,
            thickness=2,
            lineType=cv2.LINE_AA,
        )
        for pt in self.verts:
            cv2.circle(_mask, center=pt, radius=5, color=RED, thickness=-1)

        self._view = cv2.addWeighted(
            src1=self._src_raw,
            alpha=1,
            src2=_mask,
            beta=0.8,
            gamma=0,
        )
