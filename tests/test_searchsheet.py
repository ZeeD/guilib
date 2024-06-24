from typing import override
from unittest import TestCase

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from guilib.searchsheet.model import SearchableModel
from guilib.searchsheet.widget import SearchSheet


class M(QAbstractTableModel):
    MI = QModelIndex()

    def __init__(self, data: list[tuple[str, int]]) -> None:
        super().__init__()
        self._data = data

    @override
    def rowCount(
        self, _parent: QModelIndex | QPersistentModelIndex = MI
    ) -> int:
        return len(self._data)

    @override
    def columnCount(
        self, _parent: QModelIndex | QPersistentModelIndex = MI
    ) -> int:
        return 2

    @override
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | int | None:
        column = index.column()
        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[row][column])
        return None


class TestSearchSheet(TestCase):
    def test_ui(self) -> None:
        app = QApplication([])
        search_sheet = SearchSheet()
        search_sheet.set_model(
            SearchableModel(M([('uno', 101), ('due', 102), ('tre', 103)]))
        )
        search_sheet.show()
        self.assertEqual(0, app.exec())
