#!/bin/bash

# Copyright (C) 2022 b5327157
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common

[ -n "$1" ]

pushd "$(mktemp --directory)" >/dev/null

WINEPREFIX="$(readlink --canonicalize wine)"
export WINEPREFIX
export WINEDEBUG='-all,err+mscoree'
export WINEDLLOVERRIDES='winemenubuilder.exe=d'
wineboot --init

curl --location --output nuget.exe 'https://aka.ms/nugetclidl'
alias nuget-install='nuget install -DirectDownload -Verbosity quiet -NonInteractive'

wine nuget-install python
pushd python.*/tools >/dev/null
ln -s python.exe python3.10.exe
popd >/dev/null

wine nuget-install GitForWindows

winepaths=()
winepaths+=("$(winepath --windows python.*/tools)")
winepaths+=("$(winepath --windows GitForWindows.*/tools/cmd)")
printf -v WINEPATH '%s;' "${winepaths[@]}"
export WINEPATH

popd >/dev/null

exec "$@"
