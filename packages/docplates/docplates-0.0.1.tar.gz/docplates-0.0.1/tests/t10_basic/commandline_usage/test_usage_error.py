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

"""Docplates command line usage error tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestUsageError(BaseTest):
    """Docplates command line usage error test."""

    def test_no_arguments(self) -> None:  # pylint: disable=no-self-use
        """Test command line without any arguments."""

        docp_commandline = docplates.DocplatesCommandLine()

        with pytest.raises(docplates.DocplatesUsageError) as excinfo:
            docp_commandline.run([])

        assert "Nothing to do" in str(excinfo.value), "Exception information is incorrect"

    def test_invalid_commandline_argument(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid argument."""

        docp_commandline = docplates.DocplatesCommandLine()

        with pytest.raises(docplates.DocplatesUsageError) as excinfo:
            docp_commandline.run(["--does-not-exist"])

        assert "unrecognized arguments: --does-not-exist" in str(excinfo.value), "Exception information is incorrect"

    def test_invalid_output_filename_combination(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid output filename combination."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesUsageError) as excinfo:
                docp_commandline.run(["--output-file", str(test_file_dst), "--no-timestamp", str(test_file_src)])

        assert "Using --output-file and --no-timestamp or --no-subdir is pointless" in str(
            excinfo.value
        ), "Exception information is incorrect"

    def test_invalid_input_filename(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid input filename."""

        docp_commandline = docplates.DocplatesCommandLine()

        # mydir = pathlib.Path(os.path.dirname(__file__))
        # helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            # NK: We don't copy it, so it doesn't exist
            # shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--output-file", str(test_file_dst), str(test_file_src)])

        assert "Failed to locate input file" in str(excinfo.value), "Exception information is incorrect"

    def test_no_export_with_export_format(self) -> None:  # pylint: disable=no-self-use
        """Test command line with --export-format being specified without --export."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesUsageError) as excinfo:
                docp_commandline.run(["--export-format", "json", str(test_file_src)])

        assert "Using --export-format without --export makes no sense" in str(excinfo.value), "Exception information is incorrect"
