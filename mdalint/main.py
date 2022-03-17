# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDLint
# Copyright (c) 2022 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version

from pathlib import Path
import astroid

from .analysis import assign_analysis_base


def run(root: Path) -> None:
    builder = astroid.builder.AstroidBuilder()
    for file_path in root.glob('**/*.py'):
        module = builder.file_build(file_path)
        print(file_path)
        print(assign_analysis_base(module))
