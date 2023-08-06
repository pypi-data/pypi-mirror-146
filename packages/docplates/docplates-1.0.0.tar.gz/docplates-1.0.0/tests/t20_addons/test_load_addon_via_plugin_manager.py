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

"""Docplates addon via plugin manager tests."""

import os
import pathlib
import shutil
import tempfile
from typing import Dict, List

import ezplugins

import docplates

from ..base import BaseTest

__all__: List[str] = []


class TestLoadAddonViaPluginManager(BaseTest):
    """Test addons loaded via plugin manager."""

    data: Dict[str, ezplugins.EZPluginManager] = {}

    def test_module_load(self) -> None:
        """Create a plugin manager and load a plugin."""

        self.data["plugins"] = ezplugins.EZPluginManager()

        self.data["plugins"].load_module("tests.t20_addons.plugins.plugin1")

        expected_modules = [
            "tests.t20_addons.plugins.plugin1",
        ]

        received_modules = [x.module_name for x in self.data["plugins"].modules]

        assert received_modules == expected_modules, "All addons did not get loaded"

    def test_addon_tex(self) -> None:  # pylint: disable=no-self-use
        """Basic test for .tex templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_html(self) -> None:  # pylint: disable=no-self-use
        """Basic test for .html templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.html")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_tex(self) -> None:  # pylint: disable=no-self-use
        """Test includes in addons for .tex templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_html(self) -> None:  # pylint: disable=no-self-use
        """Test includes in addons for .html templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_test.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.html")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_subdir_tex(self) -> None:  # pylint: disable=no-self-use
        """Test includes with subdirs in addons for .tex templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_subdir_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_subdir_html(self) -> None:  # pylint: disable=no-self-use
        """Test includes with subdirs in addons for .tex templates."""

        docp = docplates.Docplates(config={}, plugin_manager=self.data["plugins"])

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_subdir_test.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("addon_test.html")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"
