from typing import Generic
from custom_types.generic import T


class Ref(Generic[T]):
    def __init__(self, value: T):
        self.value: T = value
