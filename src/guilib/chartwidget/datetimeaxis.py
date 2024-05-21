from datetime import date
from datetime import datetime
from enum import Enum
from enum import auto
from os import environ
from typing import TYPE_CHECKING
from typing import cast

from qtpy.QtCharts import QCategoryAxis

from guilib.chartslider.chartslider import date2days

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'


if TYPE_CHECKING:
    from collections.abc import Iterator

    from qtpy.QtCore import QDateTime
    from qtpy.QtCore import QObject


def first_january(d: date, *, before: bool = True) -> date:
    ret_year = d.year if before else d.year + 1
    return date(ret_year, 1, 1)


def next_first_of_the_month(day: date, *, delta: int = 1) -> date:
    delta_years, m = divmod(day.month - 1 + delta, 12)
    return date(day.year + delta_years, m + 1, 1)


def next_first_of_the_year(day: date, *, delta: int = 1) -> date:
    return date(day.year + delta, 1, 1)


class CreateDaysStepUnit(Enum):
    month = auto()
    year = auto()


def create_days(
    begin: date,
    end: date,
    *,
    step: int = 1,
    unit: CreateDaysStepUnit = CreateDaysStepUnit.month,
) -> 'Iterator[date]':
    """Yield all the first day of the months between begin and end."""
    day = begin
    while True:
        yield day
        op = (
            next_first_of_the_month
            if unit is CreateDaysStepUnit.month
            else next_first_of_the_year
        )
        next_day = op(day, delta=step)
        if next_day > end:
            break
        day = next_day


class DateTimeAxis(QCategoryAxis):
    def __init__(
        self,
        x_min: 'QDateTime',
        x_max: 'QDateTime',
        parent: 'QObject | None' = None,
    ) -> None:
        super().__init__(parent)
        self.setLabelsPosition(
            QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue
        )
        self.setTruncateLabels(False)

        x_min_date = cast(datetime, x_min.toPython()).date()
        x_max_date = cast(datetime, x_max.toPython()).date()

        self.setStartValue(date2days(x_min_date))

        self.min_date = x_min_date
        self.max_date = x_max_date

        self.setMin(date2days(self.min_date))
        self.setMax(date2days(self.max_date))

        self.reset_categories(unit=CreateDaysStepUnit.year)

    def reset_categories(
        self, *, unit: CreateDaysStepUnit = CreateDaysStepUnit.month
    ) -> None:
        for label in self.categoriesLabels():
            self.remove(label)

        for step in (1, 3, 4, 6, 12, 24, 36, 48):
            days = list(
                create_days(self.min_date, self.max_date, step=step, unit=unit)
            )
            if len(days) < 200:  # noqa: PLR2004 TODO: find good split
                for day in days:
                    self.append(f'{day:%Y-%m-%d}', date2days(day))
                break
