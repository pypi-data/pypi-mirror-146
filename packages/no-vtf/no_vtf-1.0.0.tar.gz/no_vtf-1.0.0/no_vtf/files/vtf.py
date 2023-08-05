# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import pathlib
import re

from typing import ClassVar, Optional, Sequence

from no_vtf.decoders.texture.vtf import VtfDecoder
from no_vtf.extractors.vtf import VtfExtractor
from no_vtf.file import File, FileFactory
from no_vtf.filter import apply_filters
from no_vtf.filters.vtf import HighestResolutionMipmapFilter
from no_vtf.image import DynamicRange, Image, ImageDataTypes
from no_vtf.namers.vtf import VTF2TGALikeNamer
from no_vtf.textures.vtf import VtfTexture


class VtfFile(File[VtfTexture]):
    @staticmethod
    def make_factory(
        *,
        mipmaps: bool = False,
        dynamic_range: Optional[DynamicRange] = None,
        overbright_factor: Optional[float] = None,
    ) -> FileFactory[VtfTexture]:
        return functools.partial(
            VtfFile,
            mipmaps=mipmaps,
            dynamic_range=dynamic_range,
            overbright_factor=overbright_factor,
        )

    def __init__(
        self,
        path: pathlib.Path,
        *,
        mipmaps: bool = False,
        dynamic_range: Optional[DynamicRange] = None,
        overbright_factor: Optional[float] = None,
    ):
        if dynamic_range is None:
            if self._hdr_file_name_pattern.search(path.name) is not None:
                dynamic_range = "hdr"
            else:
                dynamic_range = "ldr"

        self._path = path
        self._mipmaps = mipmaps
        self._dynamic_range = dynamic_range
        self._overbright_factor = overbright_factor

        self._textures: Optional[Sequence[VtfTexture]] = None

    _hdr_file_name_pattern: ClassVar[re.Pattern[str]] = re.compile(
        r"[_\.] \d*? hdr .*? \.vtf $", re.ASCII | re.IGNORECASE | re.VERBOSE
    )

    def extract(self) -> Sequence[VtfTexture]:
        if self._textures is not None:
            return list(self._textures)

        with open(self._path, "rb") as io:
            extractor = VtfExtractor()
            self._textures = extractor(io)

            filters = []
            if not self._mipmaps:
                filters.append(HighestResolutionMipmapFilter())
            self._textures = apply_filters(filters, self._textures)

        return list(self._textures)

    def name(self, texture: VtfTexture) -> str:
        name_stem = self._path.stem

        textures = self.extract()
        last_mipmap_level = max(texture.mipmap_level for texture in textures)

        namer = VTF2TGALikeNamer(include_mipmap_level=(last_mipmap_level != 0))
        return namer(name_stem, texture)

    def decode(self, texture: VtfTexture) -> Image[ImageDataTypes]:
        decoder = VtfDecoder(
            dynamic_range=self._dynamic_range, overbright_factor=self._overbright_factor
        )
        return decoder(texture)
