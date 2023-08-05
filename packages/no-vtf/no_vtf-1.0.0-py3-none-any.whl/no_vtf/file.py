# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from typing import Protocol, Sequence, TypeVar

from no_vtf.image import Image, ImageDataTypes
from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)


class File(Protocol[_TextureTypeVar]):
    @abstractmethod
    def extract(self) -> Sequence[_TextureTypeVar]:
        ...

    @abstractmethod
    def name(self, texture: _TextureTypeVar) -> str:
        ...

    @abstractmethod
    def decode(self, texture: _TextureTypeVar) -> Image[ImageDataTypes]:
        ...


class FileFactory(Protocol[_TextureTypeVar]):
    @abstractmethod
    def __call__(self, path: pathlib.Path) -> File[_TextureTypeVar]:
        ...
