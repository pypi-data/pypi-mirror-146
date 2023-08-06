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

"""Docplates addon via plugin path tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import jinja2.exceptions
import pytest

import docplates

from ..base import BaseTest

__all__: List[str] = []


class TestLoadAddonViaPath(BaseTest):
    """Test addons loaded via path."""

    def test_addon_tex(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_test.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir.mkdir(parents=True)
            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_html(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths with .html templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_test.html")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir.mkdir(parents=True)
            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_tex(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths and has an include in the addon with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_include_test.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")
        plugin_templates_someinclude = plugin_source_dir.joinpath("templates").joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_tex_include")
            test_addon_dir_templates = test_addon_dir.joinpath("templates")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir_templates.mkdir(parents=True)

            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates.joinpath("__init__.py"))
            shutil.copy(plugin_templates_someinclude, test_addon_dir_templates.joinpath("someinclude.tex"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_html(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths and has an include in the addon with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_include_test.html")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")
        plugin_templates_someinclude = plugin_source_dir.joinpath("templates").joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_html_include")
            test_addon_dir_templates = test_addon_dir.joinpath("templates")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir_templates.mkdir(parents=True)

            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates.joinpath("__init__.py"))
            shutil.copy(plugin_templates_someinclude, test_addon_dir_templates.joinpath("someinclude.html"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_subdir_tex(self) -> None:  # pylint: disable=no-self-use,too-many-locals
        """Test when an addon is loaded via config addon_paths and has an include subdir in the addon with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_include_subdir_test.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")
        plugin_templates_anotherinclude = (
            plugin_source_dir.joinpath("templates").joinpath("templates_subdir").joinpath("anotherinclude.tex")
        )

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_tex_include_subdir")
            test_addon_dir_templates = test_addon_dir.joinpath("templates")
            test_addon_dir_templates_subdir = test_addon_dir_templates.joinpath("templates_subdir")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir_templates_subdir.mkdir(parents=True)

            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates.joinpath("__init__.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates_subdir.joinpath("__init__.py"))
            shutil.copy(plugin_templates_anotherinclude, test_addon_dir_templates_subdir.joinpath("anotherinclude.tex"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_subdir_html(self) -> None:  # pylint: disable=no-self-use,too-many-locals
        """Test when an addon is loaded via config addon_paths and has an include subdir in the addon with .html templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_include_subdir_test.html")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")
        plugin_templates_anotherinclude = (
            plugin_source_dir.joinpath("templates").joinpath("templates_subdir").joinpath("anotherinclude.html")
        )

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_html_include_subdir")
            test_addon_dir_templates = test_addon_dir.joinpath("templates")
            test_addon_dir_templates_subdir = test_addon_dir_templates.joinpath("templates_subdir")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir_templates_subdir.mkdir(parents=True)

            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates.joinpath("__init__.py"))
            shutil.copy(plugin_init_py, test_addon_dir_templates_subdir.joinpath("__init__.py"))
            shutil.copy(plugin_templates_anotherinclude, test_addon_dir_templates_subdir.joinpath("anotherinclude.html"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"


class TestLoadAddonViaPathLoadFailures(BaseTest):
    """Test load addon via path failures."""

    def test_invalid_plugin_dir_name(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths and we have an invalid dir name."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_test.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_init_py = plugin_source_dir.joinpath("__init__.py")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_config_file = test_dir_path.joinpath("docplates.conf")
            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("xdocplates_addon_x_unittest_via_path_invalid_dir_name")

            test_config_file.write_text(f"addon_paths:\n  - {test_plugins_dir}", encoding="UTF-8")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir.mkdir(parents=True)
            shutil.copy(plugin_init_py, test_addon_dir.joinpath("__init__.py"))
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            with pytest.raises(jinja2.exceptions.UndefinedError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert "'test_addon_function' is undefined" in str(excinfo), "Exception information is incorrect"

    def test_no_init_py_in_plugin_dir(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths when there is no __init__.py file."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_test.tex")
        plugin_source_dir = mydir.joinpath("plugins")
        plugin_plugin1_py = plugin_source_dir.joinpath("plugin1.py")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            test_config_file = test_dir_path.joinpath("docplates.conf")
            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_addon_dir = test_plugins_dir.joinpath("docplates_addon_x_unittest_via_path_no_initpy")

            test_config_file.write_text(f"addon_paths:\n  - {test_plugins_dir}", encoding="UTF-8")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Copy plugin
            test_addon_dir.mkdir(parents=True)
            shutil.copy(plugin_plugin1_py, test_addon_dir.joinpath("plugin1.py"))

            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{test_plugins_dir}"],
                },
            )
            with pytest.raises(jinja2.exceptions.UndefinedError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert "'test_addon_function' is undefined" in str(excinfo), "Exception information is incorrect"

    def test_no_plugin_dir(self) -> None:  # pylint: disable=no-self-use
        """Test when an addon is loaded via config addon_paths when directory doesn't exist."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("addon_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            test_config_file = test_dir_path.joinpath("docplates.conf")
            test_plugins_dir = test_dir_path.joinpath("plugins")

            test_config_file.write_text(f"addon_paths:\n  - {test_plugins_dir}", encoding="UTF-8")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docplates.Docplates(
                    config={
                        "addon_paths": [f"{test_plugins_dir}"],
                    },
                )

        assert f"Add-on path '{test_plugins_dir}' does not exist" in str(excinfo), "Exception information is incorrect"
