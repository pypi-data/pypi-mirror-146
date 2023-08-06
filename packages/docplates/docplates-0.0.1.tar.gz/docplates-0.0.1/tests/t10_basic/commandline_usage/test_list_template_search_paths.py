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

"""Docplates command line list template search paths tests."""

import pathlib
import tempfile
from typing import Any, Dict, List

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestListTemplateSearchPaths(BaseTest):
    """Docplates command line list template search paths."""

    def test_list_template_search_paths_commandline(self) -> None:  # pylint: disable=no-self-use
        """Test command line list template search paths."""

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            test_dir_path = pathlib.Path(test_dir)

            # Create templates directory
            templates_path = test_dir_path.joinpath("templates")
            templates_path.mkdir()

            config_file = test_dir_path.joinpath("test.conf")
            config_file.write_text(f"template_search_paths:\n- {test_dir_path}", encoding="UTF-8")

            docp_commandline = docplates.DocplatesCommandLine()
            res = docp_commandline.run(["--config-file", str(config_file), "--list-template-search-paths"], is_api=False)

        expected: Dict[str, Any] = {"template_search_paths": [templates_path]}

        assert res is not None, "Command line option --list-template-search-paths didn't return what it is supposed to"

        assert res == expected, "Command line option --list-template-search-paths didn't return what it is supposed to"

    def test_list_template_search_paths(self) -> None:  # pylint: disable=no-self-use
        """Test command line list template search paths from API."""

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            test_dir_path = pathlib.Path(test_dir)

            # Create templates directory
            templates_path = test_dir_path.joinpath("templates")
            templates_path.mkdir()

            config_file = test_dir_path.joinpath("test.conf")
            config_file.write_text(f"template_search_paths:\n- {test_dir_path}", encoding="UTF-8")

            docp_commandline = docplates.DocplatesCommandLine()
            res = docp_commandline.run(["--config-file", str(config_file), "--list-template-search-paths"])

        expected: Dict[str, Any] = {"template_search_paths": [templates_path]}

        assert res is not None, "Command line option --list-template-search-paths didn't return what it is supposed to"

        assert res == expected, "Command line option --list-template-search-paths didn't return what it is supposed to"
