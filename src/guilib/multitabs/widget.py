from os import environ

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QTabWidget
from qtpy.QtWidgets import QToolBox
from qtpy.QtWidgets import QWidget


class MultiTabs(QTabWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setTabPosition(QTabWidget.TabPosition.West)

    def add_double_box(self, sheet: QWidget, chart: QWidget, label: str) -> int:
        return self.addTab(DoubleBox(sheet, chart, self), label)


class DoubleBox(QToolBox):
    def __init__(
        self,
        sheet: QWidget,
        chart: QWidget,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, f)
        self._sheet_idx = self.addItem(sheet, 'sheet')
        self._chart_idx = self.addItem(chart, 'chart')
