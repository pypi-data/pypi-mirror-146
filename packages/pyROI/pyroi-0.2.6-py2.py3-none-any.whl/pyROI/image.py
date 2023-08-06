from typing import NamedTuple

import numpy as np

__all__ = ["Image"]


class Image(NamedTuple):

    width: int
    height: int

    @property
    def zero_mask(self) -> np.ndarray:
        return np.zeros((self.height, self.width, 3), dtype=np.uint8)
