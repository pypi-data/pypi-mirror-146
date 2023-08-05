# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import typing

from dataclasses import dataclass
from typing import Generic, Literal, TypeAlias, TypeVar, Union

import numpy as np
import numpy.typing as npt

from no_vtf.deferrable import Deferred

DynamicRange = Literal["ldr", "hdr"]

ImageDataTypesLDR: TypeAlias = np.uint8 | np.uint16
ImageDataTypesHDR: TypeAlias = np.float16 | np.float32

ImageDataTypes: TypeAlias = Union[ImageDataTypesLDR, ImageDataTypesHDR]

ImageData: TypeAlias = npt.NDArray[ImageDataTypes]

_ImageDataTypeVar = TypeVar(
    "_ImageDataTypeVar",
    bound=ImageDataTypes,
    covariant=True,
)

ImageChannels = Literal["rgb", "rgba", "l", "la", "a"]


@dataclass(frozen=True, kw_only=True)
class Image(Generic[_ImageDataTypeVar]):
    data: Deferred[npt.NDArray[_ImageDataTypeVar]]
    dtype: npt.DTypeLike
    channels: ImageChannels

    def get_dynamic_range(self) -> DynamicRange:
        ldr = is_ldr(self.dtype)
        hdr = is_hdr(self.dtype)
        assert ldr != hdr

        return "hdr" if hdr else "ldr"


def is_ldr(dtype: npt.DTypeLike) -> bool:
    ldr_dtypes = typing.get_args(ImageDataTypesLDR)
    for ldr_dtype in ldr_dtypes:
        if np.issubdtype(dtype, ldr_dtype):
            return True

    return False


def is_hdr(dtype: npt.DTypeLike) -> bool:
    hdr_dtypes = typing.get_args(ImageDataTypesHDR)
    for hdr_dtype in hdr_dtypes:
        if np.issubdtype(dtype, hdr_dtype):
            return True

    return False
