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

"""Docplates command line invalid input file tests."""

import pathlib
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestInvalidTemplateFileError(BaseTest):
    """Docplates command line usage error test."""

    def test_non_existing_input_filename(self) -> None:  # pylint: disable=no-self-use
        """Test command line with non-existing input filename."""

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

    def test_commandline_invalid_input_filename(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid input filename."""

        docp_commandline = docplates.DocplatesCommandLine()

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            # NK: We don't copy it, so it doesn't exist
            test_file_src.mkdir()

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run([str(test_file_src)])

        assert f"Failed to locate input file '{test_file_src}'" in str(excinfo.value), "Exception information is incorrect"

    def test_docplates_invalid_input_filename(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid input filename."""

        docp = docplates.Docplates(config={})

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            # NK: We don't copy it, so it doesn't exist
            test_file_src.mkdir()

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

        assert f"Failed to locate input file '{test_file_src}'" in str(excinfo.value), "Exception information is incorrect"

    def test_invalid_input_filename_extension(self) -> None:  # pylint: disable=no-self-use
        """Test command line with invalid input filename extension."""

        docp_commandline = docplates.DocplatesCommandLine()

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.invalid-ext")

            # Copy source file
            # NK: We don't copy it, so it doesn't exist
            test_file_src.write_text("Hello world!", encoding="UTF-8")

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run([str(test_file_src)])

        assert f"No docplates backends available to handle '{test_file_src}'" in str(
            excinfo.value
        ), "Exception information is incorrect"
