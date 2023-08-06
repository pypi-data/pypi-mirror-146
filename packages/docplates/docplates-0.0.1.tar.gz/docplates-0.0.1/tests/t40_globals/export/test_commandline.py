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

"""Docplates command line export tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestExport(BaseTest):
    """Export command line test."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--output-file", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--output-file", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"

    def test_default_tex(self) -> None:  # pylint: disable=no-self-use
        """JSON export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.json")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--export", "--output-file", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_default_html(self) -> None:  # pylint: disable=no-self-use
        """JSON export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.json")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--export", "--output-file", str(test_file_dst), str(test_file_src)])

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_json_tex(self) -> None:  # pylint: disable=no-self-use
        """JSON export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.json")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                ["--output-file", str(test_file_dst), "--export", "--export-format", "json", str(test_file_src)]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_json_html(self) -> None:  # pylint: disable=no-self-use
        """JSON export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.json")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                ["--output-file", str(test_file_dst), "--export", "--export-format", "json", str(test_file_src)]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_yaml_tex(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                ["--output-file", str(test_file_dst), "--export", "--export-format", "yaml", str(test_file_src)]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_yaml_html(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                ["--output-file", str(test_file_dst), "--export", "--export-format", "yaml", str(test_file_src)]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file should of been created"

    def test_yaml_file_tex(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.pdf.export.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                [
                    "--output-file",
                    str(test_file_dst),
                    "--export",
                    "--export-format",
                    "yaml",
                    "--export",
                    str(test_file_dst_export),
                    str(test_file_src),
                ]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file not found"

    def test_yaml_file_html(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.pdf.export.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                [
                    "--output-file",
                    str(test_file_dst),
                    "--export",
                    "--export-format",
                    "yaml",
                    "--export",
                    str(test_file_dst_export),
                    str(test_file_src),
                ]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is True, "Export file not found"

    def test_yaml_stdout_tex(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.pdf.export.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                [
                    "--output-file",
                    str(test_file_dst),
                    "--export",
                    "--export-format",
                    "yaml",
                    "--export",
                    "-",
                    str(test_file_src),
                ]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is False, "Export file found"

    def test_yaml_stdout_html(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("helloworld.yaml")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(
                [
                    "--output-file",
                    str(test_file_dst),
                    "--export",
                    "--export-format",
                    "yaml",
                    "--export",
                    "-",
                    str(test_file_src),
                ]
            )

            assert test_file_dst.is_file() is True, "PDF file not generated"
            assert exports == {"export_test": "export_value"}, "Export not found"
            assert test_file_dst_export.is_file() is False, "Export file found"


class TestExportExceptions(BaseTest):
    """Export command line exception test."""

    def test_yaml_file_tex(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .tex templates with OSError exception."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("non_existing_dir").joinpath("helloworld.pdf.export")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(
                    [
                        "--export",
                        str(test_file_dst_export),
                        "--output-file",
                        str(test_file_dst),
                        str(test_file_src),
                    ]
                )

            assert "Failed to write file" in str(excinfo.value), "Exception information is incorrect"

    def test_yaml_file_html(self) -> None:  # pylint: disable=no-self-use
        """YAML export command line test for .tex templates with OSError exception."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")
            test_file_dst_export = test_dir_path.joinpath("non_existing_dir").joinpath("helloworld.pdf.export")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(
                    [
                        "--export",
                        str(test_file_dst_export),
                        "--output-file",
                        str(test_file_dst),
                        str(test_file_src),
                    ]
                )

            assert "Failed to write file" in str(excinfo.value), "Exception information is incorrect"
