# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar

from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture, contravariant=True)


class Namer(Protocol[_TextureTypeVar]):
    @abstractmethod
    def __call__(self, name_stem: str, texture: _TextureTypeVar) -> str:
        ...
