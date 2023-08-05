"""
pyROI — A simple roi selector built by python-opencv


```
import pyROI

img_path = "luna.jpg"
img = cv2.imread(img_path)

# Support rect, circle, polygon, ellipse
rect_roi = pyROI.select(src = img, selector_type =  "rect")
print(rect_roi)
# generate mask
mask = rect_roi.mask
```
"""
__author__ = "Chung-Kuan Chen (b97b01045@gmail.com)"
__version__ = "0.2.1"

from .key import *
from .circle import *
from .ellipse import *
from .image import *
from .point import *
from .polygon import *
from .rect import *
from .screen import SCREEN_HEIGHT, SCREEN_WIDTH
from .utils import *
from .window import *

__all__ = [
    # class
    "Circle",
    "Ellipse",
    "Image",
    "Point",
    "Polygon",
    "Rect",
    # function
    "calculate_distance",
    "named_window",
    "show_window",
    "select",
]
