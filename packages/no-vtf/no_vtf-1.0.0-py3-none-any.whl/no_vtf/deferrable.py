# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Callable, Generic, Optional, TypeAlias, TypeVar, cast

_DeferrableTypeVar = TypeVar("_DeferrableTypeVar", covariant=True)


class Deferred(Generic[_DeferrableTypeVar]):
    def __init__(self, thunk: Callable[[], _DeferrableTypeVar]) -> None:
        self._thunk = thunk
        self._result: Optional[_DeferrableTypeVar] = None
        self._result_valid = False

    def __call__(self) -> _DeferrableTypeVar:
        if self._result_valid:
            return cast(_DeferrableTypeVar, self._result)

        self._result = self._thunk()
        self._result_valid = True
        return self._result


Deferrable: TypeAlias = _DeferrableTypeVar | Deferred[_DeferrableTypeVar]


def to_deferred(deferrable: Deferrable[_DeferrableTypeVar]) -> Deferred[_DeferrableTypeVar]:
    if isinstance(deferrable, Deferred):
        return deferrable

    not_deferred: _DeferrableTypeVar = deferrable
    return Deferred(lambda: not_deferred)


def from_deferrable(deferrable: Deferrable[_DeferrableTypeVar]) -> _DeferrableTypeVar:
    if isinstance(deferrable, Deferred):
        return deferrable()

    return deferrable
