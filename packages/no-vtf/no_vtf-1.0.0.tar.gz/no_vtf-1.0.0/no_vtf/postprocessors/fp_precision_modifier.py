# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from dataclasses import dataclass
from typing import Literal, Optional, TypeVar

import numpy as np
import numpy.typing as npt

from no_vtf.image import ImageDataTypes
from no_vtf.postprocessor import Postprocessor

_ImageDataTypeVar = TypeVar(
    "_ImageDataTypeVar",
    bound=ImageDataTypes,
    covariant=True,
)

FloatingPointNumBits = Literal[16, 32, 64]


@dataclass(frozen=True, kw_only=True)
class FloatingPointPrecisionModifier(Postprocessor[npt.NDArray[_ImageDataTypeVar]]):
    min: Optional[FloatingPointNumBits] = None
    forced: Optional[FloatingPointNumBits] = None
    max: Optional[FloatingPointNumBits] = None

    def __post_init__(self) -> None:
        precisions = [
            precision for precision in (self.min, self.forced, self.max) if precision is not None
        ]
        precisions_sorted = sorted(precisions)
        if precisions != precisions_sorted:
            raise RuntimeError(
                f"Unordered precisions: {self.min = }, {self.forced = }, {self.max = }"
            )

    def __call__(self, data: npt.NDArray[_ImageDataTypeVar]) -> npt.NDArray[_ImageDataTypeVar]:
        if not np.issubdtype(data.dtype, np.floating):
            return data

        if self.forced is not None:
            return data.astype(f"float{self.forced}")

        fp_bits = data.dtype.itemsize * 8
        if self.min is not None and fp_bits < self.min:
            return data.astype(f"float{self.min}")
        if self.max is not None and fp_bits > self.max:
            return data.astype(f"float{self.max}")

        return data
