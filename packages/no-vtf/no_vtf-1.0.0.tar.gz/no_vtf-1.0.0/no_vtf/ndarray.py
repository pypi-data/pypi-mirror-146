# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import TYPE_CHECKING, Any, Optional, Sequence, Type, TypeVar

import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    ByteOrder = np._ByteOrder
else:
    ByteOrder = Any

_ScalarTypeVar = TypeVar("_ScalarTypeVar", bound=np.generic, covariant=True)


def image_ndarray(
    image: bytes,
    width: int,
    height: int,
    channel_order: Sequence[int],
    scalar_type: Type[_ScalarTypeVar],
    byte_order: Optional[ByteOrder] = None,
) -> npt.NDArray[_ScalarTypeVar]:
    num_channels = len(channel_order)
    shape = (height, width, num_channels)

    dtype = np.dtype(scalar_type)
    if byte_order is not None:
        dtype = dtype.newbyteorder(byte_order)

    ndarray: npt.NDArray[_ScalarTypeVar] = np.ndarray(shape=shape, dtype=dtype, buffer=image).copy()
    ndarray = ndarray[..., channel_order]
    return ndarray
