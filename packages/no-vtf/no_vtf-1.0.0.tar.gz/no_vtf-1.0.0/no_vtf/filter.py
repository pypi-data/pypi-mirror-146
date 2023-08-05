# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, Sequence, TypeVar

from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)


class Filter(Protocol[_TextureTypeVar]):
    @abstractmethod
    def __call__(self, textures: Sequence[_TextureTypeVar]) -> Sequence[_TextureTypeVar]:
        ...


def apply_filters(
    filters: Sequence[Filter[_TextureTypeVar]], textures: Sequence[_TextureTypeVar]
) -> Sequence[_TextureTypeVar]:
    for filter in filters:
        textures = filter(textures)
    return textures
