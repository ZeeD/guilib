from locale import LC_MONETARY
from locale import currency
from locale import setlocale
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast

from guilib.chartwidget.modelgui import SeriesModelUnit

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import QPointF
from qtpy.QtCore import QSizeF
from qtpy.QtCore import Qt
from qtpy.QtUiTools import QUiLoader
from qtpy.QtWidgets import QFormLayout
from qtpy.QtWidgets import QGraphicsItem
from qtpy.QtWidgets import QGraphicsLinearLayout
from qtpy.QtWidgets import QGraphicsProxyWidget
from qtpy.QtWidgets import QGraphicsWidget
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QWidget

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal

    from qtpy.QtGui import QColor


class ChartHoverUI(QWidget):
    label: QLabel
    ormLayout: QFormLayout  # noqa: N815


class ChartHover(QGraphicsWidget):
    unit: SeriesModelUnit | None = None

    def __init__(
        self, precision: str, parent: QGraphicsItem | None = None
    ) -> None:
        super().__init__(parent)
        self.setLayout(QGraphicsLinearLayout(Qt.Orientation.Vertical))
        self.setZValue(11)

        self.widget = cast(
            ChartHoverUI,
            QUiLoader().load(Path(__file__).with_name('charthoverui.ui')),
        )

        item = QGraphicsProxyWidget(self)
        item.setWidget(self.widget)
        self.keyToValueLabel: dict[str, QLabel] = {}
        self.precision = precision

    def set_unit(self, unit: SeriesModelUnit) -> None:
        self.unit = unit

    def _label(self, v: 'Decimal') -> str:
        if self.unit is SeriesModelUnit.EURO:
            setlocale(LC_MONETARY, '')
            return currency(v, grouping=True)
        return str(v)

    def set_howmuchs(
        self,
        when: 'date',
        howmuchs: dict[str, tuple['QColor', 'Decimal']],
        pos: QPointF,
    ) -> None:
        if pos == self.pos():
            return

        self.widget.label.setText(when.strftime(self.precision))

        for key, label in self.keyToValueLabel.items():
            if key not in howmuchs:
                self.widget.ormLayout.removeRow(label)
                del self.keyToValueLabel[key]
            else:
                _, v = howmuchs[key]
                label.setText(self._label(v))

        for key, (color, v) in howmuchs.items():
            if key in self.keyToValueLabel:
                continue
            label = QLabel(self._label(v), self.widget)
            label.setStyleSheet(f'background-color: {color.name()}')

            self.widget.ormLayout.addRow(key, label)
            self.keyToValueLabel[key] = label

        self.setPos(pos)

    def size(self) -> QSizeF:
        return QSizeF(self.widget.size())
