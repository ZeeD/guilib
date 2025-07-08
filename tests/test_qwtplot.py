from datetime import date
from decimal import Decimal

from _support.basetests import BaseGuiTest
from guilib.chartwidget.model import Column
from guilib.chartwidget.model import ColumnHeader
from guilib.chartwidget.model import Info
from guilib.chartwidget.viewmodel import SortFilterViewModel
from guilib.qwtplot.plot import Plot

d = date
D = Decimal

cs = [ColumnHeader(f'header{n}', 'days') for n in range(10)]

dss = [
    [D(n) for n in range(len(cs))],
    [D(-n) for n in range(len(cs))],
    [D(n + 3 if n % 2 else n // 2) for n in range(len(cs))],
    [D(2 * n) for n in range(len(cs))],
    [D(n / 3) for n in range(len(cs))],
    [D(1 - 2 * n) for n in range(len(cs))],
]

css = [[Column(c, d) for c, d in zip(cs, ds, strict=True)] for ds in dss]

ds = [
    d(2023, 12, 1),
    d(2024, 1, 1),
    d(2024, 1, 2),
    d(2024, 1, 3),
    d(2024, 1, 4),
    d(2024, 2, 1),
]

infos = [Info(d, cs) for d, cs in zip(ds, css, strict=True)]


class TestQwtPlot(BaseGuiTest):
    def test_ui(self) -> None:
        model = SortFilterViewModel()
        plot = Plot(model, None)
        plot.setWindowTitle('TestQwtPlot')
        model.update(infos)
        self.widgets.append(plot)
