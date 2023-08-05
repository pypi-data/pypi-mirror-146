# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Sequence

from no_vtf.filter import Filter
from no_vtf.textures.vtf import VtfTexture


class HighestResolutionMipmapFilter(Filter[VtfTexture]):
    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        highest_resolution_textures = [texture for texture in textures if texture.mipmap_level == 0]
        return highest_resolution_textures
