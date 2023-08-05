#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

pushd "$(mktemp --directory)" >/dev/null
curl --location --remote-name 'https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.9/kaitai-struct-compiler_0.9_all.deb'
sudo apt-get install './kaitai-struct-compiler_0.9_all.deb'
popd >/dev/null
