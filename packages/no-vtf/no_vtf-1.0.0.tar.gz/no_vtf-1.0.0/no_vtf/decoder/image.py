# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, TypeVar

from no_vtf.image import Image, ImageDataTypes

_ImageDataTypeVar = TypeVar(
    "_ImageDataTypeVar",
    bound=ImageDataTypes,
    covariant=True,
)


class ImageDecoder(Protocol[_ImageDataTypeVar]):
    @abstractmethod
    def __call__(
        self, encoded_image: bytes, logical_width: int, logical_height: int, /
    ) -> Image[_ImageDataTypeVar]:
        ...
