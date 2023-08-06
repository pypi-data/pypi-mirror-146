#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2019-2021, AllWorldIT.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Docplates test addon."""

import logging
from typing import Any, Callable, Dict, List

import ezplugins

import docplates

__all__: List[str] = []


@ezplugins.ezplugin
class Plugin1:  # pylint: disable=too-few-public-methods
    """Docplates test addon."""

    some_data: str

    def __init__(self) -> None:
        """Initialize object."""

        self.some_data = ""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_init(self, plugin_manager: ezplugins.EZPluginManager) -> None:  # pylint: disable=no-self-use,unused-argument
        """Initialize docplates addon."""

        self.some_data = "Initailized"
        logging.debug("UNITTEST PLUGIN: Unit test plugin init: %s", self.__class__)

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_globals(  # pylint: disable=unused-argument,no-self-use
        self, backend: docplates.DocplatesBackend
    ) -> Dict[str, Callable[..., Any]]:
        """
        Return our test global.

        This global is just used for testing.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        Dict[str, Callable[..., Any]] : Dict of globals to return indexed by the global name.

        """

        logging.debug("UNITTEST PLUGIN: Unit test plugin returning globals: %s", self.__class__)

        template_globals = {"test_addon_function": lambda msg: f"Message: {msg}"}

        return template_globals
