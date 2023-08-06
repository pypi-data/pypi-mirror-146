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

"""Docplates commify filter."""

from typing import Callable, Dict, List

import ezplugins

from ..backends import DocplatesBackend

__all__: List[str] = []


@ezplugins.ezplugin
class DocplatesCommifyFilterPlugin:  # pylint: disable=too-few-public-methods
    """Commify filter plugin."""

    def __init__(self) -> None:
        """Initialize object."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_filters(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., str]]:
        """
        Return commify filter.

        The commify filter returns a value like 1000 formatted as 1,000.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        Dict[str, Callable[..., :class:`str`]] :
            Dict of filter callables indexed by the filter name.

        """

        filters = {
            "commify": lambda num: f"{num:,d}",
        }

        return filters
