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

"""Docplates debug function."""

import logging
import pprint
from typing import Any, Callable, Dict, List

import ezplugins
import jinja2

from ..backends import DocplatesBackend

__all__: List[str] = []


@ezplugins.ezplugin
class DocplatesDebugFunctionPlugin:  # pylint: disable=too-few-public-methods
    """Debug function global plugin."""

    def __init__(self) -> None:
        """Initialize object."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_globals(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., Any]]:
        """
        Return debug global.

        The debug global is responsible for logging debug data about our environment.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        Dict[str, Callable[..., Any]] : Dict of globals to return indexed by the global name.

        """

        template_globals = {
            "debug": self._log_debug_data,
        }

        return template_globals

    @jinja2.pass_context
    def _log_debug_data(self, context: jinja2.runtime.Context) -> None:  # pylint: disable=no-self-use
        """
        Log debug data.

        Parameters
        ----------
        context : :class:`jinja2.runtime.Context`
            Context passed to us by Jinja2.

        """

        logging.debug(
            "Docplates: Environment Debug\n%s",
            pprint.pformat(
                {
                    "template": context.name,
                    "context": context.get_all(),
                    "filters": context.environment.filters,
                    "tests": context.environment.tests,
                    "parent": context.parent,
                    "vars": context.vars,
                    "exported_vars": context.exported_vars,
                }
            ),
        )
