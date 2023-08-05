# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: LGPL-3.0-or-later

import contextlib
import inspect
import pathlib
import sys

from typing import Optional, Sequence

import alive_progress
import click

import no_vtf

from no_vtf.file import FileFactory
from no_vtf.files.vtf import VtfFile
from no_vtf.filesystem import DirectoryFilesList
from no_vtf.image import DynamicRange
from no_vtf.pipeline import Pipeline
from no_vtf.textures.vtf import VtfTexture


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf - Valve Texture Format Converter
    Copyright (C) 2022 b5327157

    https://sr.ht/~b5327157/no_vtf/
    https://pypi.org/project/no-vtf/

    This program is free software: you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
    """

    click.echo(inspect.cleandoc(credits))
    ctx.exit()


@click.command(name="no_vtf", no_args_is_help=True)
@click.argument(
    "paths",
    metavar="PATH...",
    type=click.Path(path_type=pathlib.Path, exists=True),
    required=True,
    nargs=-1,
)
@click.option(
    "--output-dir",
    "-o",
    "output_directory",
    help="Output directory",
    type=click.Path(
        path_type=pathlib.Path, exists=True, file_okay=False, dir_okay=True, writable=True
    ),
)
@click.option(
    "--ldr-format", "-l", help="LDR output format", show_default=True, type=str, default="tiff"
)
@click.option(
    "--hdr-format", "-h", help="HDR output format", show_default=True, type=str, default="exr"
)
@click.option(
    "--dynamic-range",
    "-d",
    help="Override LDR/HDR auto-detection",
    type=click.Choice(["ldr", "hdr"], case_sensitive=False),
)
@click.option(
    "--mipmaps",
    "-m",
    help="Extract all mipmaps",
    type=bool,
    is_flag=True,
)
@click.option(
    "--separate-channels",
    "-s",
    help="Output the RGB/L and A channels separately",
    type=bool,
    is_flag=True,
)
@click.option(
    "--overbright-factor",
    "-O",
    help="Multiplicative factor used for decoding compressed HDR textures",
    show_default=True,
    type=float,
    default=16,
)
@click.option(
    "--compress/--no-compress", help="Control lossless compression", type=bool, default=None
)
@click.option("write", "--always-write/--no-write", help="Write images", type=bool, default=None)
@click.option(
    "readback", "--readback/--no-readback", help="Readback images", type=bool, default=False
)
@click.option(
    "--no-progress",
    help="Do not show the progress bar",
    type=bool,
    is_flag=True,
)
@click.version_option(version=no_vtf.__version__, message="%(version)s")
@click.option(
    "--credits",
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    ldr_format: str,
    hdr_format: str,
    dynamic_range: Optional[DynamicRange],
    mipmaps: bool,
    separate_channels: bool,
    overbright_factor: float,
    compress: Optional[bool],
    write: Optional[bool],
    readback: bool,
    no_progress: bool,
) -> None:
    """
    Convert Valve Texture Format files into standard image files.

    PATH can be either file, or directory (in which case it is recursively searched for .vtf files).
    Multiple paths may be provided.

    If the output directory is not specified, images are output into the source directories.
    Otherwise, directory tree for any found files will be reconstructed in the chosen directory.

    Output LDR/HDR format is selected by its common file name extension.
    Special formats:
    "raw" to write the high resolution image data as-is;
    "skip" to skip the write step entirely.

    For supported formats, compression is controlled when saving the image.
    Lossless compression is enabled by default. Lossy compression is not used.

    The BGRA8888 format can store both LDR and compressed HDR images.
    The specific type is either auto-detected by looking at the input file name
    (roughly, if it contains "hdr" near the end), or can be set manually.

    Only the highest-resolution mipmap is extracted by default.
    Alternatively, all mipmaps of the high-resolution image can be extracted.

    The RGB/L and A channels are packed into one file by default.
    When output separately, resulting file names will be suffixed with "_rgb", "_l" or "_a".

    By default, image files are only written if they do not exist already.
    Alternatively, they can be overwritten, or writing can be disabled entirely.

    Images can be also read back to verify they have been written properly.
    Readback will error if data to be written do not match what is in the file.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    Upon a recoverable error, conversion will proceed with the next file.
    """

    _global_config()

    directory_files_list = DirectoryFilesList.from_paths(paths)
    if directory_files_list.has_unresolved_files():
        _resolve_files(directory_files_list, not no_progress)

    pipeline = Pipeline(
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        separate_channels=separate_channels,
        compress=compress,
        write=write,
        readback=readback,
    )

    file_factory = VtfFile.make_factory(
        mipmaps=mipmaps, dynamic_range=dynamic_range, overbright_factor=overbright_factor
    )

    exit_status = _process(
        directory_files_list, output_directory, pipeline, file_factory, not no_progress
    )
    sys.exit(exit_status)


def _global_config() -> None:
    alive_progress.config_handler.set_global(spinner=None, theme="classic", enrich_print=False)


def _resolve_files(directory_files_list: DirectoryFilesList, show_progress: bool) -> None:
    progress_bar_manager = alive_progress.alive_bar(receipt=False) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for file in directory_files_list.search_in_directories("*.vtf"):
            if progress_bar:
                progress_bar.text = file.name
                progress_bar()


def _process(
    directory_files_list: DirectoryFilesList,
    output_directory: Optional[pathlib.Path],
    pipeline: Pipeline,
    file_factory: FileFactory[VtfTexture],
    show_progress: bool,
) -> int:
    exit_status = 0

    num_files = directory_files_list.num_files()
    progress_bar_manager = alive_progress.alive_bar(num_files) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for directory_files in directory_files_list:
            for file in directory_files.files:
                file_root_output_directory = output_directory or directory_files.directory
                file_relative_to_directory = file.relative_to(directory_files.directory)
                file_relative_directory = file_relative_to_directory.parent
                file_output_directory = file_root_output_directory / file_relative_directory

                if progress_bar:
                    progress_bar.text = file.name

                try:
                    texture_file = file_factory(file)
                    pipeline(texture_file, file_output_directory)

                    if progress_bar:
                        progress_bar()
                except Exception as exception:
                    exit_status = 1

                    message = f'Error while processing "{file}": {exception}'
                    if exception.__cause__:
                        message += f" ({exception.__cause__})"
                    click.echo(message, file=sys.stderr)

    return exit_status
