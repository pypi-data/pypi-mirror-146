from abc import ABC
from abc import abstractmethod
from abc import abstractproperty

from numpy import ndarray

from .point import Point
from .screen import SCREEN_HEIGHT
from .screen import SCREEN_WIDTH


class Roi(ABC):
    @abstractproperty
    def centroid(self) -> Point:
        """The centroid of the mask

        Returns:
            Point: (X, Y) namedtuple
        """

    @abstractproperty
    def mask(self) -> ndarray:
        """Generate mask(H, W, 3) based on src_size Image(W, H).

        Returns:
            ndarray: Mask (H, W, 3)
        """

    @abstractmethod
    def select(
        self,
        src: ndarray,
        *,
        winname: str = "",
        winpos_x: int = SCREEN_WIDTH // 2 - 100,
        winpos_y: int = SCREEN_HEIGHT // 2 - 100,
    ) -> "Roi":
        """

        Args:
            src (ndarray): source image for select image
            winname (str, optional): window title. Defaults to "".
            winpos_x (int, optional): window x position . Defaults to screen center.
            winpos_y (int, optional): window y position. Defaults to screen center.

        Returns:
            Roi: Return subclass[Circle/Rect/Polygon/Ellipse] derived from Roi.
        """
