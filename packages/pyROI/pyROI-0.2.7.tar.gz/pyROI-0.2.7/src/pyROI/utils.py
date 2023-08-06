from typing import Union

from numpy import ndarray

from .base import Roi
from .circle import Circle
from .ellipse import Ellipse
from .polygon import Polygon
from .rect import Rect

__all__ = ["select"]


SELECTOR_FACTORY: dict[str:Roi] = {
    "circle": Circle,
    "poly": Polygon,
    "polygon": Polygon,
    "rect": Rect,
    "rectange": Rect,
    "ellipse": Ellipse,
    "ellip": Ellipse,
}


class ImageTypeError(TypeError):
    ...


class SelectorTypeError(TypeError):
    ...


def select(
    src: ndarray,
    selector_type="rect",
    **kwargs,
) -> Union[Rect, Polygon, Circle, Ellipse]:
    """A roi select factory supporting rect/circle/polygon/ellipse selection

    Args:
        src (ndarray): target image for select region of interest
        selector_type (str, optional): _description_. Defaults to "rect".

    Raises:
        SelectorTypeError: Not rect/circle/polygon/ellipse
        ImageTypeError: only support numpy/opencv array.

    Returns:
        Union[Rect, Polygon, Circle, Ellipse]: Container class of Roi[Rect/Circle/Polygon/Ellipse]
    """
    selector = SELECTOR_FACTORY.get(selector_type.lower())
    if selector is None:
        raise SelectorTypeError(f"Only support {[*SELECTOR_FACTORY.keys()]}")

    if not isinstance(src, ndarray):
        raise ImageTypeError(src)

    return selector().select(src, **kwargs)
