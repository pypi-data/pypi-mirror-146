import pyROI as roi
import pytest
from numpy import arange
from numpy import ndarray
from numpy import random
from numpy import uint8


@pytest.fixture
def test_image() -> ndarray:
    W, H = random.choice(arange(200, 500, 50, int), 2)
    if random.choice([False, True]):
        return random.randint(0, 255, W * H * 3, dtype=uint8).reshape(H, W, 3)
    return random.randint(0, 255, W * H, dtype=uint8).reshape(H, W)


class TestSubClass:
    def test_ellipse_init(self):
        ell = roi.Ellipse()

    def test_rect_init(self):
        rect = roi.Rect()

    def test_circle_init(self):
        circle = roi.Circle()

    def test_polygon_init(self):
        poly = roi.Polygon()

    def test_retrieve_screen_resolution(self):
        assert isinstance(roi.SCREEN_WIDTH, int)
        assert isinstance(roi.SCREEN_HEIGHT, int)


class TestSubClassFucntion:
    @pytest.mark.parametrize("test_type", ["rect", "circle", "poly", "ellipse"])
    def test_roi_selector_with_params(self, test_type, test_image):
        height, width = test_image.shape[:2]
        obj = roi.select(test_image, test_type, winname=test_type)
        src_size = obj.src_size
        mask = obj.mask
        assert isinstance(mask, ndarray), test_type
        assert src_size == (width, height), test_type
        assert mask.shape[:2] == test_image.shape[:2], test_type
        assert mask.sum() != 0, test_type
