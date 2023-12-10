from os import environ
from unittest import TestCase

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCharts import QChartView
from qtpy.QtWidgets import QApplication

from guilib.multitabs.widget import MultiTabs
from guilib.searchsheet.widget import SearchSheet


class TestMultiTabs(TestCase):
    def test_ui(self) -> None:
        app = QApplication([])
        multi_tabs = MultiTabs()
        multi_tabs.add_double_box(SearchSheet(), QChartView(), 'first')
        multi_tabs.add_double_box(SearchSheet(), QChartView(), 'second')
        multi_tabs.add_double_box(SearchSheet(), QChartView(), '3rd')
        multi_tabs.show()
        self.assertEqual(0, app.exec())
