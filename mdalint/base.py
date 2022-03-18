# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDLint
# Copyright (c) 2022 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version

from typing import List, NamedTuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LineLocation:
    path: Path
    line_number: int


@dataclass
class LintWarning:
    location: LineLocation
    title: str


@dataclass
class LintError:
    location: LineLocation
    title: str


class Badge:
    name: str = 'Base Badge'

    location: LineLocation
    warnings: List[LintWarning]
    errors: List[LintError]

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

    def __str__(self):
        return (f'{self.display_name} in '
                f'{self.location.path}:{self.location.line_number}')

    @property
    def acquired(self) -> bool:
        return not bool(self.errors)

    @property
    def display_name(self) -> str:
        return self.name


class AssignResult(NamedTuple):
    badges: List[Badge]
    warnings: List[LintWarning]
    errors: List[LintError]
