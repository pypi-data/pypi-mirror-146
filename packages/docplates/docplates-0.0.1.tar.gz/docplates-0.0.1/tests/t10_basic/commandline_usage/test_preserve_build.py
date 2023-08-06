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

"""Docplates command line preserve build tests."""

import datetime
import os
import pathlib
import shutil
import tempfile
from typing import List

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestPreserveBuild(BaseTest):
    """Command line preserve build tests."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_file_dst = test_dir_path.joinpath(output_name).joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")
            build_log_file = build_dir.joinpath("helloworld.log")
            build_templated_file = build_dir.joinpath("helloworld.tex")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_log_file.is_file() is True, "Build log file not generated"
            assert build_templated_file.is_file() is True, "Build templated .tex file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_file_dst = test_dir_path.joinpath(output_name).joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is True, "Build templated .html file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_outputfile_tex(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test with output file for .tex templates."""

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
            docp_commandline.run(["--preserve-build", "--output-file", str(test_file_dst), str(test_file_src)])

            build_dir = test_file_dst.with_name("helloworld.pdf.build")
            build_log_file = build_dir.joinpath("helloworld.log")
            build_templated_file = build_dir.joinpath("helloworld.tex")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_log_file.is_file() is True, "Build log file not generated"
            assert build_templated_file.is_file() is True, "Build templated .tex file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_outputfile_html(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test with output file for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            docp_commandline.run(["--preserve-build", "--output-file", str(test_file_dst), str(test_file_src)])

            build_dir = test_file_dst.with_name("helloworld.pdf.build")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is True, "Build templated .html file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_outputfile_no_subdir_tex(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test with output file and no subdir for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_file_dst = test_dir_path.joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--preserve-build", "--no-subdir", str(test_file_src)])

            build_dir = test_file_dst.with_suffix(".pdf.build")
            build_log_file = build_dir.joinpath("helloworld.log")
            build_templated_file = build_dir.joinpath("helloworld.tex")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_log_file.is_file() is True, "Build log file not generated"
            assert build_templated_file.is_file() is True, "Build templated .tex file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_outputfile_no_subdir_html(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test with output file and no subdir for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_file_dst = test_dir_path.joinpath(f"{output_name}.pdf")

            # Generate PDF
            docp_commandline.run(["--preserve-build", "--no-subdir", str(test_file_src)])

            build_dir = test_file_dst.with_suffix(".pdf.build")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is True, "Build templated .html file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_preserve_build_dir_exists_tex(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test when build dir exists for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_pbdir_dst = test_dir_path.joinpath(output_name)
            test_file_dst = test_pbdir_dst.joinpath(f"{output_name}.pdf")

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")
            build_log_file = build_dir.joinpath("helloworld.log")
            build_templated_file = build_dir.joinpath("helloworld.tex")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            # Create the preserve build dir
            build_dir.mkdir(parents=True)

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_log_file.is_file() is True, "Build log file not generated"
            assert build_templated_file.is_file() is True, "Build templated .tex file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"

    def test_preserve_build_dir_exists_html(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test when build dir exists for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_pbdir_dst = test_dir_path.joinpath(output_name)
            test_file_dst = test_pbdir_dst.joinpath(f"{output_name}.pdf")

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            # Create the preserve build dir
            build_dir.mkdir(parents=True)

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is True, "Build templated .html file not generated"
            assert build_pdf_file.is_file() is True, "Build intermediate PDF file not generated"


class TestPreserveBuildExceptions(BaseTest):
    """Test command line preserve build exceptions."""

    def test_preserve_build_dir_exists_as_file_tex(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test when build dir exists as a file for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_pbdir_dst = test_dir_path.joinpath(output_name)
            test_file_dst = test_pbdir_dst.joinpath(f"{output_name}.pdf")

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            # Create the preserve build dir
            test_pbdir_dst.mkdir()
            build_dir.write_text("Testing", encoding="UTF-8")

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is False, "Build templated .html file generated"
            assert build_pdf_file.is_file() is False, "Build intermediate PDF file generated"

    def test_preserve_build_dir_exists_as_file_html(self) -> None:  # pylint: disable=no-self-use
        """Preserve build command line test when build dir exists as a file for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Work out the timestamp from the modification date of the file
            timestamp = datetime.datetime.fromtimestamp(test_file_src.stat().st_mtime).strftime(r"%Y%m%d%H%M")
            # Work out the output name to use
            output_name = f"{test_file_src.stem} - {timestamp}"
            test_pbdir_dst = test_dir_path.joinpath(output_name)
            test_file_dst = test_pbdir_dst.joinpath(f"{output_name}.pdf")

            build_dir = test_dir_path.joinpath(output_name).joinpath("build")

            # Create the preserve build dir
            test_pbdir_dst.mkdir()
            build_dir.write_text("Testing", encoding="UTF-8")
            build_templated_file = build_dir.joinpath("helloworld.html")
            build_pdf_file = build_dir.joinpath("helloworld.pdf")

            # Generate PDF
            docp_commandline.run(["--preserve-build", str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert build_templated_file.is_file() is False, "Build templated .html file generated"
            assert build_pdf_file.is_file() is False, "Build intermediate PDF file generated"
