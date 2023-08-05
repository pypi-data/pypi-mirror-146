# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Protocol, Sequence, TypeAlias, TypeVar

from no_vtf.image import Image, ImageDataTypes

_PostprocessorTypeVar = TypeVar("_PostprocessorTypeVar")


class Postprocessor(Protocol[_PostprocessorTypeVar]):
    # The argument is declared as positional-only, so implementations can rename it.
    # Warning: mypy does not check argument name in implementation, even if not declared as such.
    @abstractmethod
    def __call__(self, data: _PostprocessorTypeVar, /) -> _PostprocessorTypeVar:
        ...


def apply_postprocessors(
    postprocessors: Sequence[Postprocessor[_PostprocessorTypeVar]], data: _PostprocessorTypeVar
) -> _PostprocessorTypeVar:
    for postprocessor in postprocessors:
        data = postprocessor(data)
    return data


_ImageDataTypeVar = TypeVar("_ImageDataTypeVar", bound=ImageDataTypes, covariant=True)

ImagePostprocessor: TypeAlias = Postprocessor[Image[_ImageDataTypeVar]]
