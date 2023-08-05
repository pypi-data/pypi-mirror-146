#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

kaitai-struct-compiler --target python --outdir no_vtf/parsers/generated ksy/vtf.ksy
