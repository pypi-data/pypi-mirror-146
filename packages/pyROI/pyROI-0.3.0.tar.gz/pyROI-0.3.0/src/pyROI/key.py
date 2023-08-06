from enum import Enum


__all__ = ["Key"]


class Key(int, Enum):
    c = ord("c")
    q = ord("q")
    r = ord("r")
    s = ord("s")
    w = ord("w")

    C = ord("C")
    Q = ord("Q")
    R = ord("R")
    S = ord("S")
    W = ord("W")
    ENTER = ord("\r")
    ESC = ord("\x1b")
