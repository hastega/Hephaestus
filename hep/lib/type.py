from typing import Callable, TypeVar

T = TypeVar("T")
Fallback = Callable[[T], None]
ErrorFallback = Fallback[Exception]
BooleanFallback = Callable[[T], bool]
