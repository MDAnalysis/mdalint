# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDLint
# Copyright (c) 2022 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version

from typing import List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LineLocation:
    path: Path
    line_number: int


@dataclass
class BadgeWarning:
    location: LineLocation
    title: str


@dataclass
class BadgeError:
    location: LineLocation
    title: str


class Badge:
    name: str = 'Base Badge'

    location: LineLocation
    warnings: List[BadgeWarning]
    errors: List[BadgeError]

    def __init__(self, where: LineLocation):
        self.location = where
        self.warnings = []
        self.errors = []

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}: {self.name} '
            f'with {len(self.warnings)} warnings '
            f'and {len(self.errors)} errors at {id(self)}>'
        )

    @property
    def acquired(self) -> bool:
        return not bool(self.errors)
