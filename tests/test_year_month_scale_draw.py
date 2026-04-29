from datetime import date
from typing import Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from _support.basetests import BaseGuiTest
from guilib.dates.converters import date2days
from guilib.dates.generators import days
from guilib.dates.generators import months
from guilib.dates.generators import years
from guilib.qwtplot.scaledraw import YearMonthScaleDraw
from qwt.plot import QwtPlot
from qwt.plot_curve import QwtPlotCurve
from qwt.scale_div import QwtScaleDiv

LIMIT: Final = 10


def plot_and_slider(plot: QwtPlot) -> QWidget:
    ret = QWidget()
    layout = QVBoxLayout()
    ret.setLayout(layout)

    data = plot.itemList()[0].data().xData()
    data_min = int(min(data))
    data_max = int(max(data))

    slider = QSlider()
    slider.setOrientation(Qt.Orientation.Horizontal)
    slider.setMinimum(data_min)
    slider.setMaximum(data_max)

    def on_value_changed(value: int) -> None:
        ds = days(data_min, value)
        if len(ds) == 1:
            ds = []
        ms = months(data_min, value)
        if len(ms) == 1:
            ms = []
        ys = years(data_min, value)
        if len(ys) == 1:
            ys = []

        minor = ds
        medium = ms
        major = ys

        if len(medium) < LIMIT:
            medium = ds + ms
            minor = []

        if len(major) < LIMIT:
            major = ms
        if len(major) < LIMIT:
            major = ds

        plot.setAxisScaleDiv(
            QwtPlot.xBottom, QwtScaleDiv(data_min, value, minor, medium, major)
        )
        plot.replot()

    slider.valueChanged.connect(on_value_changed)
    slider.setValue(data_max)

    layout.addWidget(plot)
    layout.addWidget(slider)
    return ret


class TestYearMonthScaleDraw(BaseGuiTest):
    def test_ui(self) -> None:
        plot = QwtPlot()
        plot.setAxisScaleDraw(QwtPlot.xBottom, YearMonthScaleDraw())
        QwtPlotCurve.make(
            xdata=[
                date2days(date(2024, 1, 1)),
                date2days(date(2025, 1, 1)),
                date2days(date(2026, 1, 1)),
                date2days(date(2027, 1, 1)),
            ],
            ydata=[4, 7, 2, 5],
            plot=plot,
        )

        widget = plot_and_slider(plot)
        self.widgets.append(widget)
