# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDLint
# Copyright (c) 2022 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version

from typing import List
from pathlib import Path

import astroid
from astroid.scoped_nodes import Module
from astroid.nodes.node_ng import NodeNG

from .base import Badge, LintWarning, LintError, LineLocation, AssignResult


class AnalysisBaseBadge(Badge):
    name = 'AnalysisBase'

    def __init__(self, where, class_name):
        super().__init__(where)
        self._class_name = class_name

    @property
    def display_name(self) -> str:
        return f'{self.name}[{self._class_name}]'


def assign_analysis_base(module: Module) -> AssignResult:
    badges = []
    warnings = []
    errors = []
    results = AssignResult(badges, warnings, errors)

    analyses_nodes = (node for node in module.get_children()
                      if _is_class_inheriting(node, 'AnalysisBase'))
    for node in analyses_nodes:
        class_location = LineLocation(
            path=Path(module.file),
            line_number=node.lineno,
        )
        analysis = AnalysisBaseBadge(class_location, class_name=node.name)
        badges.append(analysis)

        has_single_frame = False
        for child in node.get_children():
            # TODO: Check that the analysis class assign values in results.
            if isinstance(child, astroid.FunctionDef):
                location = LineLocation(
                    path=Path(module.file),
                    line_number=node.lineno,
                )
                if (child.name == '_prepare'
                        and not _func_has_signature(child, 'self')):
                    analysis.warnings.append(LintWarning(
                        location=location,
                        title='_prepare method has unexpected arguments',
                    ))
                elif child.name == '_single_frame':
                    has_single_frame = True
                    if not _func_has_signature(child, 'self'):
                        analysis.warnings.append(LintWarning(
                            location=location,
                            title='_single_frame method has unexpected arguments',
                        ))
                elif (child.name == '_conclude'
                      and not _func_has_signature(child, 'self')):
                    analysis.warnings.append(LintWarning(
                        location=location,
                        title='_conclude method has unexpected arguments',
                    ))
                elif child.name == 'run':
                    if _func_has_signature(child, 'start', 'stop', 'step', 'verbose'):
                        analysis.warnings.append(BadgeWarning(
                            location=location,
                            title='The analysis class overwrites the run method.',
                        ))
                    else:
                        # TODO: This should probably be a warning and the error
                        # should probably be if arguments are not present or if
                        # the additional ones are not optional.
                        analysis.errors.append(LintError(
                            location=location,
                            title=('The analysis class overwrites the run '
                                   'method and does not use the prescribed '
                                   'signature.'),
                        ))
        if not has_single_frame:
            analysis.errors.append(LintError(
                location=class_location,
                title='The class does not define a _single_frame method.',
            ))
    return results


def _is_class_inheriting(node: NodeNG, base_name: str) -> bool:
    if isinstance(node, astroid.ClassDef) and hasattr(node, 'bases'):
        for base in node.bases:
            if hasattr(base, 'name') and base.name == base_name:
                return True
    return False


def _func_has_signature(node: NodeNG, *arguments: str) -> bool:
    if hasattr(node, 'args'):
        node_arguments = tuple(node.args.format_args().split(', '))
        return node_arguments == arguments
    return False
