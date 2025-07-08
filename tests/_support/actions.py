from functools import partial
from typing import ClassVar
from typing import Protocol
from typing import TypeVar
from typing import cast

T_contra = TypeVar('T_contra', contravariant=True)


class Consumer(Protocol):
    def __call__(self, t: T_contra) -> None: ...


class Action(Protocol):
    def __call__(self) -> None: ...


class ClassMethodWorkAround[T](Protocol):
    def __call__(self, method: type[T], /) -> None: ...
    def __get__(self, instance: None, owner: type[T]) -> Action: ...


class ClassMethod(ClassMethodWorkAround[T_contra]):
    __wrapped__: Consumer


class add_action[T]:  # noqa:N801
    actions: ClassVar[list[Action]] = []

    def __init__(self, clsmethod: ClassMethodWorkAround[T]) -> None:
        self.clsmethod = cast('ClassMethod[T]', clsmethod)

    def __get__(self, instance: None, owner: type[T]) -> Action:
        return self.clsmethod.__get__(instance, owner)

    def __set_name__(self, owner: type[T], _name: str, /) -> None:
        self.actions.append(partial(self.clsmethod.__wrapped__, owner))
