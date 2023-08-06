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

"""Docplates command line no timestamp tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestNoTimestamp(BaseTest):
    """No timestamp ommand line test."""

    def test_no_timestamp_tex(self) -> None:  # pylint: disable=no-self-use
        """No timestamp command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the output name to use
            output_name = test_file_src.stem
            test_file_dst = test_dir_path.joinpath(output_name).joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--no-timestamp", str(test_file_src)])

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_no_timestamp_html(self) -> None:  # pylint: disable=no-self-use
        """No timestamp command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the output name to use
            output_name = test_file_src.stem
            test_file_dst = test_dir_path.joinpath(output_name).joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--no-timestamp", str(test_file_src)])

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"
