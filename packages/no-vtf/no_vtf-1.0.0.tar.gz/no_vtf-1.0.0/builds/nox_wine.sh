#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

wine pip-install nox

exec wine python3.10 -m nox "$@"
