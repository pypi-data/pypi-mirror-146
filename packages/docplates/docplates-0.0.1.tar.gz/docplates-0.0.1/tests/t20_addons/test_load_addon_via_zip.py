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

"""Docplates addon via Zip tests."""

import os
import pathlib
import shutil
import tempfile
import zipfile
from typing import List

import jinja2.exceptions
import pytest

import docplates

from ..base import BaseTest

__all__: List[str] = []


class TestLoadAddonViaZip(BaseTest):
    """Test load addon via Zip file."""

    def test_addon_tex(self) -> None:  # pylint: disable=no-self-use
        """Test basic load addon via Zip file with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.tex")

        plugin_dir = mydir.joinpath("plugins")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                # Create a directory entry, this is required for Docplates
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_tex/"), "")
                addon_zip.write(plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_tex/__init__.py")
                addon_zip.write(plugin_dir.joinpath("plugin1.py"), "docplates_addon_x_unittest_via_zip_tex/plugin1.py")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_html(self) -> None:  # pylint: disable=no-self-use
        """Test basic load addon via Zip file with .html templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.html")

        plugin_dir = mydir.joinpath("plugins")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.html")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                # Create a directory entry, this is required for Docplates
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_html/"), "")
                addon_zip.write(plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_html/__init__.py")
                addon_zip.write(plugin_dir.joinpath("plugin1.py"), "docplates_addon_x_unittest_via_zip_html/plugin1.py")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_tex(self) -> None:  # pylint: disable=no-self-use
        """Test load addon via Zip file and having an include with .tex templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_test.tex")

        plugin_dir = mydir.joinpath("plugins")
        addon_test_include_file = plugin_dir.joinpath("templates").joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                # Create a directory entry, this is required for Docplates
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_include_tex/"), "")
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_include_tex/templates/"), "")
                addon_zip.write(plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_include_tex/__init__.py")
                addon_zip.write(plugin_dir.joinpath("plugin1.py"), "docplates_addon_x_unittest_via_zip_include_tex/plugin1.py")
                addon_zip.write(
                    plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_include_tex/templates/__init__.py"
                )
                addon_zip.write(addon_test_include_file, "docplates_addon_x_unittest_via_zip_include_tex/templates/someinclude.tex")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_addon_include_html(self) -> None:  # pylint: disable=no-self-use
        """Test load addon via Zip file and having an include with .html templates."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_include_test.html")

        plugin_dir = mydir.joinpath("plugins")
        addon_test_include_file = plugin_dir.joinpath("templates").joinpath("someinclude.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.html")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                # Create a directory entry, this is required for Docplates
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_include_html/"), "")
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest_via_zip_include_html/templates/"), "")
                addon_zip.write(plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_include_html/__init__.py")
                addon_zip.write(plugin_dir.joinpath("plugin1.py"), "docplates_addon_x_unittest_via_zip_include_html/plugin1.py")
                addon_zip.write(
                    plugin_dir.joinpath("__init__.py"), "docplates_addon_x_unittest_via_zip_include_html/templates/__init__.py"
                )
                addon_zip.write(
                    addon_test_include_file, "docplates_addon_x_unittest_via_zip_include_html/templates/someinclude.html"
                )

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"


class TestLoadAddonViaZipLoadFailures(BaseTest):
    """Test load addon via Zip file failures."""

    def test_invalid_component_count(self) -> None:  # pylint: disable=no-self-use
        """Test load addon via Zip file when there is a path with 3 components."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                addon_zip.writestr(zipfile.ZipInfo("somedir/docplates_addon_x_unittest_invalid_component/"), "")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )

            with pytest.raises(jinja2.exceptions.UndefinedError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert "'test_addon_function' is undefined" in str(excinfo), "Exception information is incorrect"

    def test_invalid_plugin_dir_name(self) -> None:  # pylint: disable=no-self-use
        """Test load addon via Zip file when the plugin has the wrong directory name."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                addon_zip.writestr(zipfile.ZipInfo("xdocplates_addon_x_unittest/"), "")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )

            with pytest.raises(jinja2.exceptions.UndefinedError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert "'test_addon_function' is undefined" in str(excinfo), "Exception information is incorrect"

    def test_no_init_py_in_plugin_dir(self) -> None:  # pylint: disable=no-self-use
        """Test load addon via Zip file when there is no __init__.py file."""

        mydir = pathlib.Path(os.path.dirname(__file__))
        addon_test_file = mydir.joinpath("addon_test.tex")

        plugin_dir = mydir.joinpath("plugins")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)

            test_file_src = test_dir_path.joinpath("addon_test.tex")
            test_file_dst = test_dir_path.joinpath("addon_test.pdf")

            # Create addon zip file
            zip_addon_file_dst = test_dir_path.joinpath("addon.zip")
            with zipfile.ZipFile(zip_addon_file_dst, "w") as addon_zip:
                addon_zip.writestr(zipfile.ZipInfo("docplates_addon_x_unittest/"), "")
                addon_zip.write(plugin_dir.joinpath("plugin1.py"), "docplates_addon_x_unittest/plugin1.py")

            # Copy source file
            shutil.copy(addon_test_file, test_file_src)
            # Generate PDF
            docp = docplates.Docplates(
                config={
                    "addon_paths": [f"{zip_addon_file_dst}"],
                },
            )

            with pytest.raises(jinja2.exceptions.UndefinedError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert "'test_addon_function' is undefined" in str(excinfo), "Exception information is incorrect"
