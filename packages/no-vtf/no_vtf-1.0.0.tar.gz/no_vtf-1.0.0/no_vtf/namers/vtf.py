# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass

from no_vtf.namer import Namer
from no_vtf.textures.vtf import VtfTexture


@dataclass(frozen=True, kw_only=True)
class VTF2TGALikeNamer(Namer[VtfTexture]):
    include_mipmap_level: bool

    def __call__(self, name_stem: str, texture: VtfTexture) -> str:
        if texture.face_index is not None:
            face_names = ("rt", "lf", "bk", "ft", "up", "dn", "sph")
            name_stem += face_names[texture.face_index]

        if texture.frame_index is not None:
            name_stem += f"{texture.frame_index:03d}"

        if self.include_mipmap_level:
            name_stem += f"_mip{texture.mipmap_level}"

        if texture.slice_index is not None:
            name_stem += f"_z{texture.slice_index:03d}"

        return name_stem
