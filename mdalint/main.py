# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDLint
# Copyright (c) 2022 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version

from typing import Iterable
import itertools
from pathlib import Path
import argparse

import astroid

from .base import Badge, LineLocation, LintError
from .analysis import assign_analysis_base


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    run(args.path)


def run(root: Path) -> None:
    badges = []
    warnings = []
    errors = []

    builder = astroid.builder.AstroidBuilder()
    for file_path in path_progress(root.glob('**/*.py')):
        location = LineLocation(
            path=file_path,
            line_number=0,
        )
        try:
            module = builder.file_build(file_path)
        except astroid.exceptions.AstroidSyntaxError:
            errors.append(LintError(
                location=location,
                title='Syntax error.',
            ))
            continue
        except astroid.exceptions.AstroidBuildingError:
            errors.append(LintError(
                location=location,
                title='Could not load the module.',
            ))
            continue


        badges_, warnings_, errors_ = assign_analysis_base(module)
        badges.extend(badges_)
        warnings.extend(warnings_)
        errors.extend(errors_)

    print('Acquired badges')
    print('There may be some warnings, but the conditions are '
          'fullfilled for these badges.')
    acquired_badges = (badge for badge in badges if badge.acquired)
    _display_badges(acquired_badges)

    print()

    print('Possible badges')
    print('Some conditions are met for these badges, but errors prevent '
          'them to be validated.')
    possible_badges = (badge for badge in badges if not badge.acquired)
    _display_badges(possible_badges)

    print()
    print('Errors')
    print('Besides badges, the following errors were found. These may '
          'cause issues at the execution of the tested code.')
    for error in errors:
        print(f'* {error.title}')
        print(f'  => {error.location.path}:{error.location.line_number}')

    print()
    print('Warnings')
    print('Besides badges, the following uses may not be ideal.')
    for warning in warnings:
        print(f'* {warning.title}')
        print(f'  => {warning.location.path}:{warning.location.line_number}')


def _display_badges(badges: Iterable[Badge]) -> None:
    grouped_badges = itertools.groupby(badges, key=lambda b: b.__class__)
    for badge_key, badge_group in grouped_badges:
        print(f'* {badge_key.name}')
        for badge in badge_group:
            print(f'    * {badge}')
            for warning in badge.warnings:
                print(f'        - warning: {warning.title}')
            for error in badge.errors:
                print(f'        - error: {error.title}')


def path_progress(items):
    last_line_length = 0
    for item in items:
        filler = ' ' * max(0, last_line_length - len(str(item)))
        last_line_length = len(str(item))
        print(f'\r{item}{filler}', end='')
        yield item

    filler = ' ' * len(str(item))
    print(f'\r{filler}', end='')
    print('\r', end='')
