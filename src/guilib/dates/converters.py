from datetime import date
from datetime import timedelta
from os import environ
from typing import Final

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import QDateTime

EPOCH: Final = date(1970, 1, 1)

def date2days(d: date, *, epoch: date = EPOCH) -> int:
    return (d - epoch).days

def days2date(days: float, *, epoch: date = EPOCH) -> date:
    return epoch + timedelta(days=days)

def date2QDateTime(d: date, *, epoch: date = EPOCH) -> QDateTime:
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))

