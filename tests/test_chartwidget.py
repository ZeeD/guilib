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

from qtpy.QtCore import QCoreApplication
from qtpy.QtCore import Qt
from qtpy.QtQuick import QQuickWindow
from qtpy.QtQuick import QSGRendererInterface
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
        infos: 'list[Info]' = [
            I(date(2023, 1, 1), [C(CH('foo'), Decimal('0'))]),
            I(date(2023, 1, 2), [C(CH('foo'), Decimal('100'))]),
            I(date(2023, 1, 4), [C(CH('foo'), Decimal('200'))]),
            I(date(2023, 1, 8), [C(CH('foo'), Decimal('300'))]),
            I(date(2023, 1, 16), [C(CH('foo'), Decimal('400'))]),
            I(date(2023, 2, 1), [C(CH('foo'), Decimal('500'))]),
            I(date(2023, 3, 1), [C(CH('foo'), Decimal('600'))]),
            I(date(2023, 4, 1), [C(CH('foo'), Decimal('700'))]),
            I(date(2023, 6, 1), [C(CH('foo'), Decimal('800'))]),
            I(date(2024, 1, 15), [C(CH('foo'), Decimal('0'))]),
            I(date(2024, 1, 15), [C(CH('foo'), Decimal('5000'))]),
            I(date(2024, 2, 1), [C(CH('foo'), Decimal('5000'))]),
            I(date(2024, 2, 1), [C(CH('foo'), Decimal('1000'))]),
            I(date(2024, 3, 1), [C(CH('foo'), Decimal('1000'))]),
            I(date(2024, 3, 1), [C(CH('foo'), Decimal('3000'))]),
            I(date(2024, 4, 1), [C(CH('foo'), Decimal('3000'))]),
            I(date(2024, 4, 1), [C(CH('foo'), Decimal('2000'))]),
        ]

        model = SortFilterViewModel()
        factory = SeriesModel.by_column_header(CH('foo'))

        QCoreApplication.setAttribute(
            Qt.ApplicationAttribute.AA_ShareOpenGLContexts
        )
        QQuickWindow.setGraphicsApi(
            QSGRendererInterface.GraphicsApi.OpenGLRhi  # @UndefinedVariable
        )

        app = QApplication([])
        widget = ChartWidget(model, None, factory, '%d/%m/%Y')
        model.update(infos)
        widget.resize(800, 600)
        widget.show()
        self.assertEqual(0, app.exec())
