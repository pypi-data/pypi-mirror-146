# no_vtf

Say no to .vtf – convert it to one of the standard image formats.

[![Badge showing package version on PyPI](https://img.shields.io/pypi/v/no_vtf?style=flat-square)](https://pypi.org/project/no-vtf/)
[![Badge showing number of monthly downloads from PyPI](https://img.shields.io/pypi/dm/no_vtf?style=flat-square)](https://pypi.org/project/no-vtf/)
![Badge showing supported Python versions](https://img.shields.io/pypi/pyversions/no_vtf?style=flat-square)

![Screencast showing conversion of sprays downloaded in Team Fortress 2 using no_vtf](https://git.sr.ht/~b5327157/no_vtf/blob/HEAD/resources/docs/screencast.gif)

## Motivation

- cross-platform – runs on any machine where Python is supported
- console-only – runs without a graphical interface
- full HDR support (including [compressed HDR](https://developer.valvesoftware.com/wiki/Valve_Texture_Format#HDR_compression))
- proper decoding of the `ARGB8888` format
- formally described .vtf file format (via [Kaitai Struct](https://kaitai.io))
- regression suite against crafted .vtf files and reference output

## Installation

### Application bundle

For Linux and Windows running on x64, there are application bundles with the Python interpreter included.

- [no_vtf-linux_x64.tar.xz](https://b5327157.srht.site/no_vtf/release/no_vtf-linux_x64.tar.xz) (glibc 2.31 or newer required, i.e. Debian 11, Ubuntu 20.04 LTS, …)
- [no_vtf-windows_x64.zip](https://b5327157.srht.site/no_vtf/release/no_vtf-windows_x64.zip) (Windows 8.1 or newer required)

```
./no_vtf ...  # Linux
no_vtf.exe ...  %= Windows =%
```

Bundles are ready to be used offline – the FreeImage library is already included.

### Package

If you have Python 3.10 or newer, you can install the package from PyPI directly:

```
python3 -m pip install no_vtf

python3 -m no_vtf ...
```

Or install it into a virtual environment:

```
python3 -m venv no_vtf-venv

source no_vtf-venv/bin/activate  # Linux
no_vtf-venv/scripts/activate  %= Windows =%

no_vtf ...
```

Before the first conversion, the FreeImage library will be downloaded to support the process. Further conversions are supported offline.

## Usage

#### General invocation

```
no_vtf [OPTIONS] PATH...
```

PATH can be either file or directory. Multiple paths may be provided.

Tip: With bundles, drag-and-drop files or folders to be converted onto the application launcher (the file with icon and no extension on Linux and the .exe file on Windows).

#### Change output directory

```
no_vtf --output-dir /tmp PATH...
```

#### Override LDR/HDR output format

```
no_vtf --ldr-format png --hdr-format tiff PATH...
```

#### Further help

```
no_vtf --help
```

## Supported formats

### Input

All textures installed with Team Fortress 2 and Source Filmmaker can be converted with the supported format set.

- `RGBA8888`
- `ABGR8888`
- `RGB888`
- `BGR888`
- `I8`
- `IA88`
- `A8`
- `RGB888_BLUESCREEN`
- `BGR888_BLUESCREEN`
- `ARGB8888`
- `BGRA8888`
- `DXT1`
- `DXT3`
- `DXT5`
- `DXT1_ONEBITALPHA`
- `UV88`
- `RGBA16161616F`
- `RGBA16161616`

### Output

The following formats were tested and optimized for use:

#### LDR

- PNG
- TGA
- TIFF (default)

#### HDR

- EXR (default)
- TIFF

It is also possible to select other [formats](https://imageio.readthedocs.io/en/stable/formats/index.html) supported by Imageio.

## Known issues

### Color space

Color space of LDR textures is inferred from the context in which the texture is used in-game. Since this context is not available when converting the .vtf files directly, color space metadata for the output images cannot be set.

Color space of HDR textures is always linear. It would make sense to set this metadata when converting into the TIFF format, but for technical reasons, this is not done.

### Opaque PNG

When using PNG, the alpha channel is not written when the image is fully opaque. This may pose problems in other programs. In Blender, for example, when such image is not packed and OSL is enabled, the alpha channel is shown as black. For this reason, TIFF is the default LDR format instead of PNG.

## Benchmark

#### Environment

- Sample: 11 GiB of LDR .vtf files
- CPU: Intel Core i7-6500U

#### Terminology

Time is the total CPU time spent in user and kernel mode.
Size is the total disk usage consumed by the output.
Conversion was done without extraction of all mipmaps.

### Uncompressed

- PNG: 10.35 minutes
- TGA: 2.69 minutes
- TIFF: 3.27 minutes

In all three cases, the size was 33 GiB.

### Compressed

- PNG: 5.9 GiB, 12.56 minutes
- TGA: 14 GiB, 3.77 minutes
- TIFF: 6.9 GiB, 8.81 minutes

## Development

For more resources, check out the Nox sessions in `noxfile.py` and the build system in `builds/`.

### Linting

```
python3 -m pip install nox

python3 -m nox -R
python3 -m nox -R -- --fix
```

### Pre-build steps

```
# compile .ksy files (requires Kaitai Struct compiler)
# only necessary if a .ksy file was modified
ksy/compile.sh
```
