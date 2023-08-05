# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Iterable, Optional, TypeVar

import numpy.typing as npt

from no_vtf.deferrable import Deferrable, Deferred, from_deferrable
from no_vtf.image import Image, ImageDataTypes

_ImageDataTypeVar = TypeVar(
    "_ImageDataTypeVar",
    bound=ImageDataTypes,
    contravariant=True,
)


class ChannelSeparator:
    def __call__(
        self, image: Deferrable[Image[_ImageDataTypeVar]]
    ) -> Iterable[Image[_ImageDataTypeVar]]:
        image = from_deferrable(image)

        data_rgb: Optional[Deferred[npt.NDArray[_ImageDataTypeVar]]] = None
        data_l: Optional[Deferred[npt.NDArray[_ImageDataTypeVar]]] = None
        data_a: Optional[Deferred[npt.NDArray[_ImageDataTypeVar]]] = None

        match (image.channels):
            case "rgb":
                data_rgb = image.data
            case "rgba":
                data_rgb = _index_channels(image.data, slice(0, 3))
                data_a = _index_channels(image.data, slice(3, 4))
            case "l":
                data_l = image.data
            case "la":
                data_l = _index_channels(image.data, slice(0, 1))
                data_a = _index_channels(image.data, slice(1, 2))
            case "a":
                data_a = image.data
            case _:
                raise RuntimeError(f"Unsupported channel configuration: {image.channels}")

        if data_rgb is not None:
            yield Image(data=data_rgb, dtype=image.dtype, channels="rgb")

        if data_l is not None:
            yield Image(data=data_l, dtype=image.dtype, channels="l")

        if data_a is not None:
            yield Image(data=data_a, dtype=image.dtype, channels="a")


def _index_channels(
    data: Deferrable[npt.NDArray[_ImageDataTypeVar]], channels: slice
) -> Deferred[npt.NDArray[_ImageDataTypeVar]]:
    def thunk() -> npt.NDArray[_ImageDataTypeVar]:
        _data = from_deferrable(data)
        _data = _data[..., channels]
        return _data

    return Deferred(thunk)
