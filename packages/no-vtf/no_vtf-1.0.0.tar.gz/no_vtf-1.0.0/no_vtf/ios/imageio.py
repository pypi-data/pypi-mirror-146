# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import pathlib
import re

from dataclasses import dataclass
from typing import ClassVar, Optional, cast

import imageio
import imageio.plugins.freeimage
import numpy as np
import numpy.typing as npt

from no_vtf.deferrable import Deferrable, from_deferrable
from no_vtf.image import Image, ImageData, ImageDataTypes
from no_vtf.io import Io
from no_vtf.postprocessor import Postprocessor
from no_vtf.postprocessors.fp_precision_modifier import FloatingPointPrecisionModifier


@dataclass(frozen=True, kw_only=True)
class Imageio(Io[Image[ImageDataTypes]]):

    _format_pattern: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9]+", re.ASCII | re.IGNORECASE)

    _freeimage_requested: ClassVar[bool] = False

    @classmethod
    def request_freeimage(cls) -> None:
        if cls._freeimage_requested:
            return

        imageio.plugins.freeimage.download()

        cls._freeimage_requested = True

    format: str

    compress: Optional[bool] = None

    def __post_init__(self) -> None:
        if not self._format_pattern.fullmatch(self.format):
            raise RuntimeError(f"Invalid format: {self.format}")

    def write(self, path: pathlib.Path, image: Deferrable[Image[ImageDataTypes]]) -> None:
        backend = self._get_backend()
        data = self._get_data(image)

        backend.write(path, data)

    def readback(self, path: pathlib.Path, image: Deferrable[Image[ImageDataTypes]]) -> None:
        backend = self._get_backend()
        data = self._get_data(image)

        backend.readback(path, data)

    def _get_backend(self) -> ImageioBackend:
        compress = self.compress
        if compress is None:
            compress = True

        backend: ImageioBackend
        match self.format.lower():
            case "exr":
                backend = ImageioExrBackend(compress=compress)
            case "png":
                backend = ImageioPngBackend(compress=compress)
            case "targa" | "tga":
                backend = ImageioTgaBackend(compress=compress)
            case "tiff":
                backend = ImageioTiffBackend(compress=compress)
            case _:
                backend = ImageioBackend()
        return backend

    def _get_data(self, image: Deferrable[Image[ImageDataTypes]]) -> ImageData:
        image = from_deferrable(image)
        data = image.data()

        # write luminance into three channels when alpha is present
        if image.channels == "la":
            l_uint8: npt.NDArray[np.uint8] = data[:, :, [0]]
            a_uint8: npt.NDArray[np.uint8] = data[:, :, [1]]
            data = np.dstack((l_uint8, l_uint8, l_uint8, a_uint8))

        # remove last axis if its length is 1
        if data.shape[-1] == 1:
            data = data[..., 0]

        return data


class ImageioBackend:
    def __init__(self, *, _imageio_format: Optional[str] = None) -> None:
        self._imageio_format = _imageio_format

    def write(self, path: pathlib.Path, data: ImageData) -> None:
        kwargs = self._get_writer_kwargs(data)
        data = self._postprocess(data)
        with imageio.get_writer(path, format=self._imageio_format, mode="i", **kwargs) as writer:
            writer.append_data(data)

    def readback(self, path: pathlib.Path, data: ImageData) -> None:
        data = self._postprocess(data)
        with imageio.get_reader(path, format=self._imageio_format, mode="i") as reader:
            read_data = reader.get_data(index=0)

            if data.dtype != read_data.dtype:
                raise RuntimeError("Data type differs from what is in the file")

            if not self._compare(data, read_data):
                raise RuntimeError("Data differs from what is in the file")

    def _get_writer_kwargs(self, data: ImageData) -> dict[str, object]:
        return {}

    def _postprocess(self, data: ImageData) -> ImageData:
        return data

    def _compare(self, data: ImageData, read_data: ImageData) -> bool:
        return np.array_equal(data, read_data)


class ImageioFreeImageBackend(ImageioBackend):
    IO_FLAGS: ClassVar = imageio.plugins.freeimage.IO_FLAGS

    def __init__(self, *, _imageio_format: str) -> None:
        super().__init__(_imageio_format=_imageio_format)

    def _get_writer_kwargs(self, data: ImageData) -> dict[str, object]:
        kwargs: dict[str, object] = {}
        kwargs["flags"] = self._get_flags(data)
        return kwargs

    def _get_flags(self, data: ImageData) -> int:
        return 0


class ImageioExrBackend(ImageioFreeImageBackend):
    _fp_force_32_bits: ClassVar[Postprocessor[ImageData]] = FloatingPointPrecisionModifier(
        forced=32
    )

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(_imageio_format="EXR-FI")
        self.compress = compress

    def _get_flags(self, data: ImageData) -> int:
        flags = 0
        flags |= self.IO_FLAGS.EXR_ZIP if self.compress else self.IO_FLAGS.EXR_NONE
        if not np.issubdtype(data.dtype, np.float16):
            flags |= self.IO_FLAGS.EXR_FLOAT
        return flags

    def _postprocess(self, data: ImageData) -> ImageData:
        return self._fp_force_32_bits(data)


class ImageioPngBackend(ImageioFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(_imageio_format="PNG-FI")
        self.compress = compress

    def _get_writer_kwargs(self, data: ImageData) -> dict[str, object]:
        kwargs: dict[str, object] = super()._get_writer_kwargs(data)
        kwargs["compression"] = 1 if self.compress else 0
        return kwargs

    def _compare(self, data: ImageData, read_data: ImageData) -> bool:
        if np.issubdtype(data.dtype, np.uint8) and np.issubdtype(read_data.dtype, np.uint8):
            if read_data.ndim == 3 and read_data.shape[2] == 3:
                data = _strip_opaque_alpha(cast(npt.NDArray[np.uint8], data))

        return super()._compare(data, read_data)


class ImageioTgaBackend(ImageioFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(_imageio_format="TARGA-FI")
        self.compress = compress

    def _get_flags(self, data: ImageData) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TARGA_SAVE_RLE if self.compress else self.IO_FLAGS.TARGA_DEFAULT
        return flags


class ImageioTiffBackend(ImageioFreeImageBackend):
    _fp_force_32_bits: ClassVar[Postprocessor[ImageData]] = FloatingPointPrecisionModifier(
        forced=32
    )

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(_imageio_format="TIFF-FI")
        self.compress = compress

    def _get_flags(self, data: ImageData) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TIFF_DEFAULT if self.compress else self.IO_FLAGS.TIFF_NONE
        return flags

    def _postprocess(self, data: ImageData) -> ImageData:
        return self._fp_force_32_bits(data)


def _strip_opaque_alpha(data: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    if data.ndim == 3 and data.shape[2] == 4 and np.all(data[..., 3] == 255):
        data = data[..., :3]

    return data
