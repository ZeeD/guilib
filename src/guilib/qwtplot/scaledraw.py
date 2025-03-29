from qwt.scale_draw import QwtScaleDraw

from guilib.dates.converters import days2date


class EuroScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return f'€ {value:_.2f}'


class YearMonthScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return days2date(value).strftime('%Y-%m')
