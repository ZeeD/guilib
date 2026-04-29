from collections.abc import Sequence
from typing import Literal
from typing import overload

from qwt.interval import QwtInterval

class QwtScaleDiv:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, lowerBound: float, upperBound: float) -> None: ...
    @overload
    def __init__(
        self, lowerBound: float, upperBound: float, ticks: list[Sequence[float]]
    ) -> None: ...
    @overload
    def __init__(
        self,
        lowerBound: float,
        upperBound: float,
        minorTicks: Sequence[float],
        mediumTicks: Sequence[float],
        majorTicks: Sequence[float],
    ) -> None: ...
    def setLowerBound(self, lowerBound: float) -> None: ...
    def setUpperBound(self, upperBound: float) -> None: ...
    def interval(self) -> QwtInterval: ...
    MinorTick: Literal[0]
    MediumTick: Literal[1]
    MajorTick: Literal[2]
    def ticks(self, tickType: Literal[0, 1, 2]) -> list[float]: ...
    def setTicks(
        self, tickType: Literal[0, 1, 2], ticks: list[float]
    ) -> None: ...
