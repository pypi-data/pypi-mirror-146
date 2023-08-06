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

"""Docplates raise function."""

from typing import Any, Callable, Dict, List

import ezplugins
import jinja2.exceptions

from ..backends import DocplatesBackend

__all__: List[str] = []


@ezplugins.ezplugin
class DocplatesRaiseFunctionPlugin:  # pylint: disable=too-few-public-methods
    """Raise function global plugin."""

    def __init__(self) -> None:
        """Initialize object."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_globals(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., Any]]:
        """
        Return raise global.

        The raise global allows raising an exception within a template.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        Dict[str, Callable[..., Any]] : Dict of globals to return indexed by the global name.

        """

        template_globals = {
            "raise": self._raise,
        }

        return template_globals

    def _raise(self, message: str) -> None:  # pylint: disable=no-self-use
        """
        Raise an exception.

        Parameters
        ----------
        message : :class:`str`
            Context passed to us by Jinja2.

        """

        raise jinja2.exceptions.TemplateRuntimeError(message)
