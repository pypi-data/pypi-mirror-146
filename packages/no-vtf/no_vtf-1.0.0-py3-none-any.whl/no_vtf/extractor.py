# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import BinaryIO, Protocol, Sequence, TypeVar

from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture, covariant=True)


class Extractor(Protocol[_TextureTypeVar]):
    @abstractmethod
    def __call__(self, io: BinaryIO) -> Sequence[_TextureTypeVar]:
        ...
