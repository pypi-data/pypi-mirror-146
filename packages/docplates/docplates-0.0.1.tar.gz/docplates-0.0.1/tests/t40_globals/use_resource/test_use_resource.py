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

"""Docplates built-in use_resource tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestUseResource(BaseTest):
    """Use resource command line builtin test."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Use resource command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")
        helloworld_image_file = mydir.joinpath("image.png")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_src_image = test_dir_path.joinpath("image.png")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(helloworld_image_file, test_file_src_image)

            # Generate PDF
            docp_commandline.run(["--output", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Use resource command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")
        helloworld_css_file = mydir.joinpath("helloworld.css")
        helloworld_image_file = mydir.joinpath("image.png")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_src_image = test_dir_path.joinpath("image.png")
            test_file_src_css = test_dir_path.joinpath("helloworld.css")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(helloworld_css_file, test_file_src_css)
            shutil.copy(helloworld_image_file, test_file_src_image)

            # Generate PDF
            exports = docp_commandline.run(["--output", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            # For the HTML file which includes a rendered CSS file we check for the export set in the CSS file
            assert exports == {"export_test": "export_value"}, "Export not found"


class TestUseResourceErrors(BaseTest):
    """Test use_resource errors."""

    def test_resource_does_not_exist(self) -> None:  # pylint: disable=no-self-use
        """Use resource command line test for when the resource doesn't exist."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_resource_not_exist.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--output", str(test_file_dst), str(test_file_src)])

        assert "Resource 'image_not_exist.png' not found" in str(excinfo.value), "Exception information is incorrect"
