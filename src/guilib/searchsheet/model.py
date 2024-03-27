from os import environ

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'
from qtpy.QtCore import QAbstractItemModel
from qtpy.QtCore import QObject
from qtpy.QtCore import QSortFilterProxyModel
from qtpy.QtCore import Qt


class SearchableModel(QSortFilterProxyModel):
    def __init__(
        self, model: QAbstractItemModel, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self.setSourceModel(model)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
