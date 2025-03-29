from typing import TYPE_CHECKING
from typing import Protocol
from typing import override

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import date
    from decimal import Decimal


class ColumnHeaderProto(Protocol):
    name: str
    # TODO: add unit


class ColumnProto(Protocol):
    header: ColumnHeaderProto
    howmuch: 'Decimal | None'


class InfoProto(Protocol):
    when: 'date'
    columns: 'Sequence[ColumnProto]'

    def howmuch(self, column_header: ColumnHeaderProto) -> 'Decimal | None': ...


# default impl


class ColumnHeader:
    def __init__(self, name: str) -> None:
        self.name = name

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ColumnHeader):
            return NotImplemented
        return self.name == other.name


class Column:
    def __init__(
        self, header: 'ColumnHeaderProto', howmuch: 'Decimal | None'
    ) -> None:
        self.header = header
        self.howmuch = howmuch


class Info:
    def __init__(self, when: 'date', columns: 'Sequence[ColumnProto]') -> None:
        self.when = when
        self.columns = columns

    def howmuch(self, column_header: 'ColumnHeaderProto') -> 'Decimal | None':
        for column in self.columns:
            if column.header == column_header:
                return column.howmuch
        return None
