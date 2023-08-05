# opencv-roi
pyROI — A simple roi selector built by python-opencv


# Installation

- from pypi
```console
> pip install pyROI
```

- from github
```console
> pip install -U git+https://github.com/lycantrope/pyROI
```
# Usage

```python
import pyROI

img_path = "luna.jpg"
img = cv2.imread(img_path)

# Support rect, circle, polygon, ellipse
rect_roi = pyROI.select(src = img, selector_type =  "rect")
print(rect_roi)

# generate mask
mask = rect_roi.mask
```
