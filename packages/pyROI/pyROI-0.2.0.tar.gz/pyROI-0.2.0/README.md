# opencv-roi
pyROI — A simple roi selector built by python-opencv


# Installation

```console
> pip install -U git+https://github.com/lycantrope/pyROI
```

# Usage

```python
import pyROI

# Support rect, circle, polygon, ellipse
img_path = "luna.jpg"
img = cv2.imread(img_path)  
rect_roi = pyROI.select(src = img, selector_type =  "rect")
print(rect_roi)

```
