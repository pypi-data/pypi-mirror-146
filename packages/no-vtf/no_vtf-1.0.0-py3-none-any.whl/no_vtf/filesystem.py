# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import collections
import pathlib

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence


class DirectoryFiles:
    def __init__(self, path: pathlib.Path) -> None:
        self.directory: pathlib.Path
        self.files: list[pathlib.Path]

        if path.is_dir():
            self.directory = path
            self.files = []
        else:
            self.directory = path.parent
            self.files = [path]

    def search_in_directory(self, pattern: str) -> Iterable[pathlib.Path]:
        assert not self.files

        for file in self.directory.rglob(pattern):
            self.files.append(file)
            yield file


class DirectoryFilesList(collections.UserList[DirectoryFiles]):
    @staticmethod
    def from_paths(paths: Sequence[pathlib.Path]) -> DirectoryFilesList:
        directory_files_list = DirectoryFilesList()
        for path in paths:
            directory_files = DirectoryFiles(path)
            directory_files_list.append(directory_files)
        return directory_files_list

    def __init__(self, initlist: Optional[Iterable[DirectoryFiles]] = None):
        super().__init__(initlist)

    def num_files(self) -> int:
        num_files = 0
        for files in self._files_list():
            num_files += len(files)
        return num_files

    def has_unresolved_files(self) -> bool:
        return not all(self._files_list())

    def search_in_directories(self, pattern: str) -> Iterable[pathlib.Path]:
        for directory_files in self.data:
            if not directory_files.files:
                for file in directory_files.search_in_directory(pattern):
                    yield file

    def _files_list(self) -> Sequence[Sequence[pathlib.Path]]:
        return list(map(lambda directory_files: directory_files.files, self.data))


@dataclass(frozen=True, kw_only=True)
class FileAccessor:
    skip_existing: bool = False
    mkdir_missing_parents: bool = False

    def __call__(self, path: pathlib.Path) -> bool:
        if self.skip_existing and path.is_file():
            return False

        if self.mkdir_missing_parents:
            path.parent.mkdir(parents=True, exist_ok=True)

        return True
