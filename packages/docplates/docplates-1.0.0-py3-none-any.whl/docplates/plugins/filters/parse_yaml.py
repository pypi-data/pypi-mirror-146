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

"""Docplates parse_yaml filter."""

from typing import Any, Callable, Dict, List

import ezplugins
import jinja2.exceptions
import yaml
import yaml.parser
import yaml.scanner

from ..backends import DocplatesBackend

__all__: List[str] = []


@ezplugins.ezplugin
class DocplatesRaiseFunctionPlugin:  # pylint: disable=too-few-public-methods
    """Parse YAML filter plugin."""

    def __init__(self) -> None:
        """Initialize object."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_filters(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., Any]]:
        """
        Return a structure based on a parsed YAML string.

        The prase_yaml filter allows parsing of a YAML string into a structure.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        Dict[str, Callable[..., Any]] : Dict of filters to return indexed by the filter name.

        """

        template_filters = {
            "parse_yaml": self._parse_yaml,
        }

        return template_filters

    def _parse_yaml(self, yamlstr: str) -> Any:  # pylint: disable=no-self-use
        """
        Parse YAML string into a structure.

        Parameters
        ----------
        yamlstr : :class:`str`
            String to parse.

        Returns
        -------
        :class:`Any` :
            Parsed structure.

        """

        try:
            return yaml.safe_load(yamlstr)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as exc:
            raise jinja2.exceptions.TemplateRuntimeError(f"Failed to parse YAML: {exc}") from None
