from datetime import datetime
from datetime import time
from typing import override

from guilib.dates.converters import days2date
from qwt.scale_draw import QwtDateTimeScaleDraw
from qwt.scale_draw import QwtScaleDraw
from qwt.text import QwtText


class EuroScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> QwtText:
        return QwtText.make(f'€ {value:_.2f}')


class YearMonthScaleDraw(QwtDateTimeScaleDraw):
    def __init__(self) -> None:
        super().__init__('%Y\n%m-%d')

    @override
    def label(self, value: float) -> 'QwtText':
        return super().label(
            datetime.combine(days2date(value), time()).timestamp()
        )
