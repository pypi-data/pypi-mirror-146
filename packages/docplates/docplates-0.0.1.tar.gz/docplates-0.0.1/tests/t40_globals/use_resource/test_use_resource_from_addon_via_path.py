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

"""Docplates built-in use_resource tests for addons via path."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestUseResourceLoadAddonViaPath(BaseTest):
    """Test resources loaded from addons via path."""

    def test_addon(self) -> None:  # pylint: disable=no-self-use
        """Test when a resource is loaded with an addon when loaded via a path."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_use_from_lib.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")
        plugin_image_png = mydir.joinpath("image.png")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_use_resource_via_path")
            test_addon_dir_templates = test_addon_dir.joinpath("templates")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir_templates.mkdir(parents=True)
            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates.joinpath("__init__.py"))
            shutil.copy(plugin_image_png, test_addon_dir_templates.joinpath("image.png"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"
