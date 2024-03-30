from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from os import environ
from typing import TYPE_CHECKING

from guilib.chartslider.chartslider import EPOCH
from guilib.chartslider.chartslider import date2days

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCharts import QLineSeries
from qtpy.QtCore import QDateTime

if TYPE_CHECKING:
    from .model import ColumnHeader
    from .model import Info


class SeriesModelUnit(Enum):
    EURO = auto()
    HOUR = auto()
    DAY = auto()


def date2QDateTime(d: 'date', *, epoch: 'date' = EPOCH) -> 'QDateTime':  # noqa: N802
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))


SeriesModelFactory = Callable[['list[Info]'], 'SeriesModel']


@dataclass
class SeriesModel:
    series: 'list[QLineSeries]'
    x_min: 'QDateTime'
    x_max: 'QDateTime'
    y_min: float
    y_max: float
    unit: 'SeriesModelUnit'

    @staticmethod
    def by_column_header(
        *column_headers: 'ColumnHeader',
    ) -> 'SeriesModelFactory':
        def factory(infos: 'list[Info]') -> 'SeriesModel':
            x_min = date.max
            x_max = date.min
            y_min = Decimal('inf')
            y_max = Decimal(0)

            line_seriess = []
            for column_header in column_headers:
                line_series = QLineSeries()
                line_series.setName(column_header.name)
                for info in infos:
                    when = info.when
                    howmuch = info.howmuch(column_header) or Decimal(0)

                    if when < x_min:
                        x_min = when
                    if when > x_max:
                        x_max = when

                    if howmuch < y_min:
                        y_min = howmuch
                    if howmuch > y_max:
                        y_max = howmuch

                    line_series.append(date2days(when), float(howmuch))
                line_seriess.append(line_series)

            return SeriesModel(
                line_seriess,
                date2QDateTime(x_min),
                date2QDateTime(x_max),
                float(y_min),
                float(y_max),
                SeriesModelUnit.EURO,
            )

        return factory
