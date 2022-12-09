from typing import Generic
from custom_types.generic import T


class Ref(Generic[T]):
    """Provides reference semantics for a type.

    Useful for when an immutable type needs to be passed into a function
    as if it was mutable (i.e., like a reference).
    """

    def __init__(self, value: T):
        self.value: T = value
