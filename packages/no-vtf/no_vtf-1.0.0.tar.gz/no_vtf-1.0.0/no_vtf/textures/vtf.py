# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import dataclasses

from dataclasses import dataclass
from typing import Optional, cast

from no_vtf.parsers.generated.vtf import Vtf as VtfParser
from no_vtf.texture import Texture


@dataclass(frozen=True, kw_only=True)
class VtfTexture(Texture):
    mipmap_level: int
    frame_index: Optional[int]
    face_index: Optional[int]
    slice_index: Optional[int]

    image: VtfParser.Image = dataclasses.field(repr=False, hash=False)

    def get_width(self) -> int:
        return cast(int, self.image.logical_width)

    def get_height(self) -> int:
        return cast(int, self.image.logical_height)

    def get_data(self) -> bytes:
        return cast(bytes, self.image.image_data)
