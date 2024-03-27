from os import environ
from typing import TYPE_CHECKING

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import QItemSelectionModel
from qtpy.QtCore import QSortFilterProxyModel
from qtpy.QtCore import Qt
from qtpy.QtGui import QKeySequence
from qtpy.QtGui import QShortcut
from qtpy.QtWidgets import QAbstractItemView
from qtpy.QtWidgets import QAbstractScrollArea
from qtpy.QtWidgets import QGridLayout
from qtpy.QtWidgets import QLineEdit
from qtpy.QtWidgets import QTableView
from qtpy.QtWidgets import QWidget

if TYPE_CHECKING:
    from .model import SearchableModel


class SearchSheet(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, f)

        self.table_view = QTableView(self)
        self.table_view.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_view.setShowGrid(True)
        self.table_view.setGridStyle(Qt.PenStyle.DashLine)
        self.table_view.setSortingEnabled(True)
        self.table_view.setWordWrap(False)
        self.table_view.horizontalHeader().setCascadingSectionResizes(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText('Filter')
        self.line_edit.textChanged.connect(self._line_edit_changed)

        layout = QGridLayout(self)
        layout.addWidget(self.table_view, 0, 0, 1, 1)
        layout.addWidget(self.line_edit, 1, 0, 1, 1)
        self.setLayout(layout)

        QShortcut(QKeySequence('Ctrl+F'), self).activated.connect(
            self.line_edit.setFocus
        )
        QShortcut(QKeySequence('Esc'), self).activated.connect(
            lambda: self.line_edit.setText('')
        )

    def _line_edit_changed(self, text: str) -> None:
        model = self.table_view.model()
        if isinstance(model, QSortFilterProxyModel):
            model.setFilterWildcard(text)

    def set_model(self, searchable_model: 'SearchableModel') -> None:
        self.table_view.setModel(searchable_model)
        searchable_model.modelReset.connect(
            self.table_view.resizeColumnsToContents
        )

    def selection_model(self) -> QItemSelectionModel:
        return self.table_view.selectionModel()
