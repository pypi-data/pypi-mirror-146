import typing

from .python_qa.utils.classes import T


def filtered(func: typing.Callable[[T], bool], iterable: typing.Iterable[T]):
    return type(iterable)(filter(func, iterable))
