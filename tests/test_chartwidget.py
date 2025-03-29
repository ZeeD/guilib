from datetime import date
from decimal import Decimal
from typing import Final

from _support.basetests import BaseGuiTest
from guilib.chartwidget.chartwidget import ChartWidget
from guilib.chartwidget.model import Column
from guilib.chartwidget.model import ColumnHeader
from guilib.chartwidget.model import Info
from guilib.chartwidget.modelgui import SeriesModel
from guilib.chartwidget.viewmodel import SortFilterViewModel


class TestChartWidget(BaseGuiTest):
    header: Final = ColumnHeader('foo')
    infos: Final = [
        Info(date(2023, 1, 1), [Column(header, Decimal('0'))]),
        Info(date(2023, 1, 2), [Column(header, Decimal('100'))]),
        Info(date(2023, 1, 4), [Column(header, Decimal('200'))]),
        Info(date(2023, 1, 8), [Column(header, Decimal('300'))]),
        Info(date(2023, 1, 16), [Column(header, Decimal('400'))]),
        Info(date(2023, 2, 1), [Column(header, Decimal('500'))]),
        Info(date(2023, 3, 1), [Column(header, Decimal('600'))]),
        Info(date(2023, 4, 1), [Column(header, Decimal('700'))]),
        Info(date(2023, 6, 1), [Column(header, Decimal('800'))]),
        Info(date(2024, 1, 15), [Column(header, Decimal('0'))]),
        Info(date(2024, 1, 15), [Column(header, Decimal('5000'))]),
        Info(date(2024, 2, 1), [Column(header, Decimal('5000'))]),
        Info(date(2024, 2, 1), [Column(header, Decimal('1000'))]),
        Info(date(2024, 3, 1), [Column(header, Decimal('1000'))]),
        Info(date(2024, 3, 1), [Column(header, Decimal('3000'))]),
        Info(date(2024, 4, 1), [Column(header, Decimal('3000'))]),
        Info(date(2024, 4, 1), [Column(header, Decimal('2000'))]),
    ]

    def test_ui(self) -> None:
        model = SortFilterViewModel()
        widget = ChartWidget(
            model, None, SeriesModel.by_column_header(self.header), '%d/%m/%Y'
        )
        model.update(self.infos)
        widget.setWindowTitle('TestChartWidget')
        widget.resize(800, 600)
        self.widgets.append(widget)
