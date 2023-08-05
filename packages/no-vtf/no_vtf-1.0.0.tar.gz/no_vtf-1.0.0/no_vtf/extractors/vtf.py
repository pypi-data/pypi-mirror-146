# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass
from typing import BinaryIO, Optional, Sequence, cast

import kaitaistruct

from no_vtf.extractor import Extractor
from no_vtf.parsers.generated.vtf import Vtf as VtfParser
from no_vtf.textures.vtf import VtfTexture


@dataclass(frozen=True, kw_only=True)
class VtfExtractor(Extractor[VtfTexture]):
    def __call__(self, io: BinaryIO) -> Sequence[VtfTexture]:
        try:
            parser = VtfParser.from_io(io)
        except kaitaistruct.KaitaiStructError as exception:
            raise RuntimeError("Parser error") from exception

        high_res_image = self._high_res_image_7_0(parser) or self._high_res_image_7_3(parser)
        if not high_res_image:
            return ()

        textures = self._textures_from_high_res_image(parser, high_res_image)
        return textures

    def _high_res_image_7_0(self, parser: VtfParser) -> Optional[VtfParser.HighResImage]:
        return getattr(parser.body, "high_res_image", None)

    def _high_res_image_7_3(self, parser: VtfParser) -> Optional[VtfParser.HighResImage]:
        resources = getattr(parser.body, "resources", None)
        if not resources:
            return None

        for resource in resources:
            high_res_image: Optional[VtfParser.HighResImage] = getattr(
                resource, "high_res_image", None
            )
            if high_res_image:
                return high_res_image

        return None

    def _textures_from_high_res_image(
        self, parser: VtfParser, high_res_image: VtfParser.HighResImage
    ) -> Sequence[VtfTexture]:
        has_multiple_frames = parser.header.v7_0.num_frames > 1
        is_cubemap = parser.header.logical.flags.envmap
        has_multiple_slices = parser.header.logical.num_slices > 1

        textures: list[VtfTexture] = []
        for mipmap in high_res_image.image_mipmaps:
            mipmap = cast(VtfParser.ImageMipmap, mipmap)
            mipmap_level = parser.header.v7_0.num_mipmaps - mipmap.mipmap_index - 1

            frame_index: Optional[int]
            for frame_index, frame in enumerate(mipmap.image_frames):
                frame_index = frame_index if has_multiple_frames else None
                frame = cast(VtfParser.ImageFrame, frame)

                face_index: Optional[int]
                for face_index, face in enumerate(frame.image_faces):
                    face_index = face_index if is_cubemap else None
                    face = cast(VtfParser.ImageFace, face)

                    slice_index: Optional[int]
                    for slice_index, slice in enumerate(face.image_slices):
                        slice_index = slice_index if has_multiple_slices else None
                        slice = cast(VtfParser.Image, slice)

                        texture = VtfTexture(
                            mipmap_level=mipmap_level,
                            frame_index=frame_index,
                            face_index=face_index,
                            slice_index=slice_index,
                            image=slice,
                        )
                        textures.append(texture)
        return textures
