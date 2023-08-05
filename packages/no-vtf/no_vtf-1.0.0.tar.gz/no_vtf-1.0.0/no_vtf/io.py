# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from typing import Protocol, TypeVar

from no_vtf.deferrable import Deferrable

_IoTypeVar = TypeVar("_IoTypeVar", contravariant=True)


class Io(Protocol[_IoTypeVar]):
    @abstractmethod
    def write(self, path: pathlib.Path, data: Deferrable[_IoTypeVar]) -> None:
        ...

    @abstractmethod
    def readback(self, path: pathlib.Path, data: Deferrable[_IoTypeVar]) -> None:
        ...
