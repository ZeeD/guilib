from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QToolBox
from PySide6.QtWidgets import QWidget


class MultiTabs(QTabWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setTabPosition(QTabWidget.TabPosition.West)

    def add_double_box(self, sheet: QWidget, chart: QWidget, label: str) -> int:
        return self.addTab(DoubleBox(sheet, chart, self), label)

    def remove_double_box(self, idx: int) -> None:
        self.removeTab(idx)


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
        sheet.setParent(self, f)
        chart.setParent(self, f)
