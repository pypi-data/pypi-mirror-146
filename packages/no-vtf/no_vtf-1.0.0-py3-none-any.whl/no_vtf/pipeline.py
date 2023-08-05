# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from dataclasses import dataclass
from typing import Literal, Optional, TypeVar

from no_vtf.channel_separator import ChannelSeparator
from no_vtf.file import File
from no_vtf.filesystem import FileAccessor
from no_vtf.image import Image, ImageDataTypes
from no_vtf.io import Io
from no_vtf.ios.bytes_io import BytesIo
from no_vtf.ios.imageio import Imageio
from no_vtf.texture import Texture

_TextureTypeVar = TypeVar("_TextureTypeVar", bound=Texture)
_IoTypeVar = TypeVar("_IoTypeVar", contravariant=True)


@dataclass(frozen=True, kw_only=True)
class Pipeline:
    FORMAT_RAW: Literal["raw"] = "raw"
    FORMAT_SKIP: Literal["skip"] = "skip"

    ldr_format: str
    hdr_format: str

    separate_channels: bool = False

    compress: Optional[bool] = None

    write: Optional[bool] = None
    readback: bool = False

    def __post_init__(self) -> None:
        Imageio.request_freeimage()

    def __call__(self, input_file: File[_TextureTypeVar], output_directory: pathlib.Path) -> None:
        textures = input_file.extract()
        for texture in textures:
            image = input_file.decode(texture)
            dynamic_range = image.get_dynamic_range()

            format = self.hdr_format if dynamic_range == "hdr" else self.ldr_format
            if _compare_formats(format, self.FORMAT_SKIP):
                continue

            name_stem = input_file.name(texture)
            output_name = name_stem + "." + format
            output_path = output_directory / output_name

            if _compare_formats(format, self.FORMAT_RAW):
                bytes_io = BytesIo()
                data = texture.get_data()
                self._do_io(bytes_io, output_path, data)
            else:
                imageio = Imageio(format=format, compress=self.compress)
                if not self.separate_channels:
                    self._do_io(imageio, output_path, image)
                else:
                    self._separate_channels(imageio, output_path, image)

    def _separate_channels(
        self, imageio: Imageio, path: pathlib.Path, image: Image[ImageDataTypes]
    ) -> None:
        channel_separator = ChannelSeparator()
        for image_separated in channel_separator(image):
            new_stem = path.stem + "_" + image_separated.channels
            new_path = path.with_stem(new_stem)
            self._do_io(imageio, new_path, image_separated)

    def _do_io(self, io: Io[_IoTypeVar], path: pathlib.Path, data: _IoTypeVar) -> None:
        if self.write is not False:
            self._write(io, path, data)

        if self.readback:
            io.readback(path, data)

    def _write(self, io: Io[_IoTypeVar], path: pathlib.Path, data: _IoTypeVar) -> None:
        skip_existing = self.write is None
        file_accessor = FileAccessor(
            skip_existing=skip_existing,
            mkdir_missing_parents=True,
        )

        if file_accessor(path):
            io.write(path, data)


def _compare_formats(a: str, b: str) -> bool:
    return a.lower() == b.lower()
