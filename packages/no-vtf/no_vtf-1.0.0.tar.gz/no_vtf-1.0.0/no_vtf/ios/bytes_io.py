# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from no_vtf.deferrable import Deferrable, from_deferrable
from no_vtf.io import Io


class BytesIo(Io[bytes]):
    def write(self, path: pathlib.Path, data: Deferrable[bytes]) -> None:
        data = from_deferrable(data)

        with open(path, "wb") as file:
            file.write(data)

    def readback(self, path: pathlib.Path, data: Deferrable[bytes]) -> None:
        data = from_deferrable(data)

        with open(path, "rb") as file:
            read_data = file.read()
            if data != read_data:
                raise RuntimeError("Data differs from what is in the file")
