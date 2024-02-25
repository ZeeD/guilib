from abc import abstractmethod
from datetime import date
from datetime import timedelta
from logging import error
from pathlib import Path
from typing import Final
from typing import cast
from typing import override

from qtpy.QtCore import QSortFilterProxyModel
from qtpy.QtCore import Qt
from qtpy.QtCore import QUrl
from qtpy.QtCore import Signal
from qtpy.QtCore import Slot
from qtpy.QtQuick import QQuickItem
from qtpy.QtQuick import QQuickView
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

EPOCH: Final = date(1970, 1, 1)


def date2days(d: date, *, epoch: date = EPOCH) -> int:
    return (d - epoch).days


def days2date(days: float, *, epoch: date = EPOCH) -> date:
    return epoch + timedelta(days=days)


class RangeSlider(QQuickItem):
    first_moved: Signal
    second_moved: Signal

    @abstractmethod
    def set_first_value(
        self,
        first_value: float,  # @UnusedVariable
    ) -> None:
        ...

    @abstractmethod
    def set_second_value(
        self,
        second_value: float,  # @UnusedVariable
    ) -> None:
        ...


class RangeSliderView(QQuickView):
    def __init__(self) -> None:
        super().__init__(
            QUrl.fromLocalFile(Path(__file__).with_name('chartslider.qml'))
        )
        self.statusChanged.connect(self.dump)
        self.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)

    def dump(self, status: QQuickView.Status) -> None:
        if status is QQuickView.Status.Error:
            for error_ in self.errors():
                error('error=%s', error_)

    @override
    def rootObject(self) -> RangeSlider:
        return cast(RangeSlider, super().rootObject())


class ChartSlider(QWidget):
    start_date_changed = Signal(date)
    end_date_changed = Signal(date)

    def __init__(
        self, model: QSortFilterProxyModel, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.view = RangeSliderView()

        self.range_slider = self.view.rootObject()

        container = QWidget.createWindowContainer(self.view)
        container.setMinimumSize(100, 10)
        layout.addWidget(container)

        self._model = model
        self._model.sourceModel().modelReset.connect(self.source_model_reset)

        def _start_date_changed(days: int) -> None:
            self.start_date_changed.emit(days2date(days))

        self.range_slider.first_moved.connect(_start_date_changed)

        def _end_date_changed(days: int) -> None:
            self.end_date_changed.emit(days2date(days))

        self.range_slider.second_moved.connect(_end_date_changed)

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self._model.sourceModel()
        dates: list[date] = [
            source_model.data(
                source_model.createIndex(row, 0), Qt.ItemDataRole.UserRole
            )
            for row in range(source_model.rowCount())
        ]
        if not dates:
            error('no dates!')
            return
        dates.sort()
        minimum = date2days(dates[0])
        maximum = date2days(dates[-1])

        self.range_slider.setProperty('from', minimum)
        self.range_slider.setProperty('to', maximum)
        self.range_slider.set_first_value(minimum)
        self.range_slider.set_second_value(maximum)