from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette

from qwt.scale_div import QwtScaleDiv
from qwt.text import QwtText

class QwtScaleDraw:
    def label(self, value: float) -> QwtText: ...
    def scaleDiv(self) -> QwtScaleDiv: ...
    def draw(self, painter: QPainter, palette: QPalette) -> None: ...

class QwtDateTimeScaleDraw(QwtScaleDraw):
    def __init__(self, format: str = ...) -> None: ...  # noqa: A002
