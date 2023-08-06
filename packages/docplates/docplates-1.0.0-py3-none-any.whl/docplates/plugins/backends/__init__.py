#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2015-2020, AllWorldIT.
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

"""Docplates backends."""

import pathlib
from typing import Dict, List

__all__ = [
    "DocplatesBackend",
]


class DocplatesBackend:
    """
    Docplates base backend class.

    Docplates backends inherit from this class.

    """

    _template_extensions: List[str]
    _resource_extensions: List[str]
    _jinja_environment_options: Dict[str, str]

    def __init__(self) -> None:
        """
        Docplates base backend class.

        Docplates backends inherit from this class.

        """

        self._template_extensions = []
        self._resource_extensions = []
        self._jinja_environment_options = {}

    def render(self, template_file_path: pathlib.Path) -> pathlib.Path:
        """
        Render the template file.

        Parameters
        ----------
        template_file_path : :class:`pathlib.path`
            Template file path to render.

        Returns
        -------
        :class:`pathlib.Path` :
            Rendered file's path.

        """
        raise NotImplementedError

    @property
    def resource_extensions(self) -> List[str]:
        """
        Resource file extensions supported by the backend.

        Returns
        -------
        :class:`List` [ :class:`str` ] :
            List of resource file extensions supported.

        """
        return self._resource_extensions

    @property
    def template_extensions(self) -> List[str]:
        """
        Template file extensions supported by the backend.

        Returns
        -------
        :class:`List` [ :class:`str` ] :
            List of template file extensions supported.

        """
        return self._template_extensions

    @property
    def jinja_environment_options(self) -> Dict[str, str]:
        """
        Jinja environment options for this backend.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`str` ] :
            Dict of Jinja2 environment options for this backend.

        """
        return self._jinja_environment_options
