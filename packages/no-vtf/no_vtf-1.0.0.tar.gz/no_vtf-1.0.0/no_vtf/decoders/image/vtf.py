# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Optional

import numpy as np
import numpy.typing as npt

from no_vtf.decoders.image.generic import (
    decode_bgr_uint8,
    decode_bgra_uint8,
    decode_rgb_uint8,
    decode_rgba_uint16_le,
)
from no_vtf.deferrable import Deferred
from no_vtf.image import Image


def decode_rgb_uint8_bluescreen(encoded_image: bytes, width: int, height: int) -> Image[np.uint8]:
    image = decode_rgb_uint8(encoded_image, width, height)
    image = _decode_bluescreen(image)
    return image


def decode_bgr_uint8_bluescreen(encoded_image: bytes, width: int, height: int) -> Image[np.uint8]:
    image = decode_bgr_uint8(encoded_image, width, height)
    image = _decode_bluescreen(image)
    return image


def _decode_bluescreen(image: Image[np.uint8]) -> Image[np.uint8]:
    assert image.channels == "rgb"

    def thunk() -> npt.NDArray[np.uint8]:
        rgb_uint8 = image.data()

        is_opaque: npt.NDArray[np.bool_] = rgb_uint8 != (0, 0, 255)
        is_opaque = is_opaque.any(axis=2)
        is_opaque = is_opaque[..., np.newaxis]

        rgb_uint8 *= is_opaque
        a_uint8: npt.NDArray[np.uint8] = np.multiply(is_opaque, 255, dtype=np.uint8)

        rgba_uint8: npt.NDArray[np.uint8] = np.dstack((rgb_uint8, a_uint8))
        return rgba_uint8

    return Image(data=Deferred(thunk), dtype=np.uint8, channels="rgba")


def decode_bgra_uint8_hdr(
    encoded_image: bytes, width: int, height: int, overbright_factor: Optional[float]
) -> Image[np.float32]:
    if overbright_factor is None:
        overbright_factor = 16

    def thunk() -> npt.NDArray[np.float32]:
        rgba_uint8 = decode_bgra_uint8(encoded_image, width, height).data()

        rgba_float32: npt.NDArray[np.float32] = rgba_uint8.astype(np.float32) / 255.0
        rgba_float32[:, :, [0, 1, 2]] *= rgba_float32[:, :, [3]] * overbright_factor

        rgb_float32: npt.NDArray[np.float32] = rgba_float32[..., :3]
        return rgb_float32

    return Image(data=Deferred(thunk), dtype=np.float32, channels="rgb")


def decode_rgba_uint16_le_hdr(encoded_image: bytes, width: int, height: int) -> Image[np.float32]:
    def thunk() -> npt.NDArray[np.float32]:
        rgba_uint16 = decode_rgba_uint16_le(encoded_image, width, height).data()
        # convert 4.12 fixed point stored as integer into floating point
        rgba_float32: npt.NDArray[np.float32] = rgba_uint16.astype(np.float32) / (1 << 12)
        return rgba_float32

    return Image(data=Deferred(thunk), dtype=np.float32, channels="rgba")
