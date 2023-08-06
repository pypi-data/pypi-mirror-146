#
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2015-2022, AllWorldIT.
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

"""Docplates command line list plugins tests."""

from typing import List

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestListPlugins(BaseTest):
    """Docplates command line list plugins test."""

    def test_list_plugins_commandline(self) -> None:  # pylint: disable=no-self-use
        """Test command line list plugins."""

        docp_commandline = docplates.DocplatesCommandLine()
        res = docp_commandline.run(["--list-plugins"], is_api=False)

        expected = {
            "plugins": [
                "docplates.plugins.backends.latex",
                "docplates.plugins.backends.weasyprint",
                "docplates.plugins.filters.commify",
                "docplates.plugins.filters.parse_yaml",
                "docplates.plugins.globals.debug",
                "docplates.plugins.globals.logger",
                "docplates.plugins.globals.raise_global",
            ]
        }

        assert res is not None, "Command line option --list-plugins didn't return what it is supposed to"

        assert res == expected, "Command line option --list-plugins didn't return what it is supposed to"

    def test_list_plugins(self) -> None:  # pylint: disable=no-self-use
        """Test command line list plugins from API."""

        docp_commandline = docplates.DocplatesCommandLine()
        res = docp_commandline.run(["--list-plugins"])

        expected = {
            "plugins": [
                "docplates.plugins.backends.latex",
                "docplates.plugins.backends.weasyprint",
                "docplates.plugins.filters.commify",
                "docplates.plugins.filters.parse_yaml",
                "docplates.plugins.globals.debug",
                "docplates.plugins.globals.logger",
                "docplates.plugins.globals.raise_global",
            ]
        }

        assert res is not None, "Command line option --list-plugins didn't return what it is supposed to"

        assert res == expected, "Command line option --list-plugins didn't return what it is supposed to"
