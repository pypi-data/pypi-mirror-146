#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2015-2022, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Docplates exceptions."""

import argparse
from typing import Any

import jinja2

__all__ = [
    "DocplatesError",
    "DocplatesUsageError",
    "DocplatesResourceNotFoundError",
]


class DocplatesError(RuntimeError):
    """Docplates runtime error."""


class DocplatesUsageError(RuntimeError):
    """Docplates runtime error, raised when used incorrectly."""

    message: str
    parser: argparse.ArgumentParser

    def __init__(self, *args: Any):
        """Initialize object."""

        super().__init__(*args)

        self.message = args[0]
        self.parser = args[1]

    def __str__(self) -> str:
        """Return string representation of the exception."""

        return f"{self.message}\n\n{self.parser.format_help()}"


class DocplatesResourceNotFoundError(jinja2.TemplateNotFound, DocplatesError):  # pylint: disable=too-many-ancestors
    """Docplates resource not found error."""
