from typing import Tuple
from custom_types.basic import Char
from custom_types.generic import T


GridData = Tuple[
    T, T, T, T, T, T, T, T, T, T,
    T, T, T, T, T, T, T, T, T, T,
    T, T,
]

EventCode = Tuple[Char, Char, Char, Char]

CarCornerData = Tuple[T, T, T, T]


# TODO: move
TyreStintData = Tuple[T, T, T, T, T, T, T, T]


# TODO: move
Name = Tuple[
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
]
