from datetime import date
from decimal import Decimal

from _support.basetests import BaseGuiTest
from guilib.chartwidget.model import Column
from guilib.chartwidget.model import ColumnHeader
from guilib.chartwidget.model import Info
from guilib.chartwidget.viewmodel import SortFilterViewModel
from guilib.qwtplot.plot import Plot

UNO = ColumnHeader('uno')
DUE = ColumnHeader('due')

d = date
D = Decimal


class TestQwtPlot(BaseGuiTest):
    def test_ui(self) -> None:
        model = SortFilterViewModel()
        plot = Plot(model, None)
        plot.setWindowTitle('TestQwtPlot')
        model.update(
            [
                Info(d(2023, 12, 1), [Column(UNO, D(0)), Column(DUE, D(0))]),
                Info(d(2024, 1, 1), [Column(DUE, D(1))]),
                Info(d(2024, 1, 2), [Column(DUE, D(2))]),
                Info(d(2024, 1, 3), [Column(UNO, D(3)), Column(DUE, D(4))]),
                Info(d(2024, 1, 4), [Column(UNO, D(5))]),
                Info(d(2024, 2, 1), [Column(UNO, D(0)), Column(DUE, D(0))]),
            ]
        )
        self.widgets.append(plot)
