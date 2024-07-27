import functools
from typing import Any, Callable, TypeAlias

ComposableFunctions: TypeAlias = Callable[[Any], Any]


def compose(*funcs: ComposableFunctions) -> ComposableFunctions:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), funcs)
