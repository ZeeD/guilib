from datetime import date
from decimal import Decimal
from os import environ
from typing import TYPE_CHECKING
from typing import override
from unittest import TestCase

from guilib.chartwidget.chartwidget import ChartWidget
from guilib.chartwidget.modelgui import SeriesModel
from guilib.chartwidget.viewmodel import SortFilterViewModel

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtWidgets import QApplication

if TYPE_CHECKING:
    from guilib.chartwidget.model import Column
    from guilib.chartwidget.model import ColumnHeader
    from guilib.chartwidget.model import Info


class CH:
    def __init__(self, name: str) -> None:
        self.name = name

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CH):
            return NotImplemented
        return self.name == other.name


class C:
    def __init__(
        self, header: 'ColumnHeader', howmuch: 'Decimal | None'
    ) -> None:
        self.header = header
        self.howmuch = howmuch


class I:  # noqa: E742
    def __init__(self, when: 'date', columns: 'list[Column]') -> None:
        self.when = when
        self.columns = columns

    def howmuch(self, column_header: 'ColumnHeader') -> 'Decimal | None':
        for column in self.columns:
            if column.header == column_header:
                return column.howmuch
        return None


class TestChartWidget(TestCase):
    def test_ui(self) -> None:
        app = QApplication([])

        infos: 'list[Info]' = [
            I(
                date(2024, 1, 1),
                [
                    C(CH('foo'), Decimal('1')),
                    C(CH('bar'), Decimal('2')),
                    C(CH('baz'), Decimal('3')),
                ],
            ),
            I(
                date(2024, 2, 1),
                [
                    C(CH('foo'), Decimal('7')),
                    C(CH('bar'), Decimal('8')),
                    C(CH('baz'), Decimal('9')),
                ],
            ),
            I(
                date(2024, 3, 1),
                [
                    C(CH('foo'), Decimal('4')),
                    C(CH('bar'), Decimal('5')),
                    C(CH('baz'), Decimal('6')),
                ],
            ),
        ]

        model = SortFilterViewModel()
        factory = SeriesModel.by_column_header(CH('foo'))

        widget = ChartWidget(model, None, factory)
        model.update(infos)
        widget.show()
        self.assertEqual(0, app.exec())
