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

"""Docplates command line load data tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestLoadData(BaseTest):
    """Test command line load data."""

    def test_loaddata_yaml_tex(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile.yaml")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert exports == {"data_test": {"testitem": "testvalue"}}, "Export data from load not correct"

    def test_loaddata_yaml_html(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.html")
        data_file = mydir.joinpath("datafile.yaml")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert exports == {"data_test": {"testitem": "testvalue"}}, "Export data from load not correct"

    def test_loaddata_json_tex(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile.json")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert exports == {"data_test": {"testitem": "testvalue"}}, "Export data from load not correct"

    def test_loaddata_json_html(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data for .html templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.html")
        data_file = mydir.joinpath("datafile.json")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert exports == {"data_test": {"testitem": "testvalue"}}, "Export data from load not correct"


class TestLoadDataExceptions(BaseTest):
    """Test command line load data exceptions."""

    def test_loaddata_file_not_exist(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data for .tex templates."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile-does-not-exist.yaml")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert "Data file does not exist" in str(excinfo.value), "Exception raised is incorrect"

    def test_loaddata_invalid_json(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data with invalid JSON."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile_invalid.json")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert "Error loading JSON data file" in str(excinfo.value), "Exception raised is incorrect"

    def test_loaddata_invalid_yaml(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data with invalid YAML."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile_invalid.yaml")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert "Error loading YAML data file" in str(excinfo.value), "Exception raised is incorrect"

    def test_loaddata_invalid_extension(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data with invalid extension."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile_invalid_extension.dat")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert "has unsupported extension" in str(excinfo.value), "Exception raised is incorrect"

    def test_loaddata_invalid_type(self) -> None:  # pylint: disable=no-self-use
        """Test command line load data with invalid type."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_export_data.tex")
        data_file = mydir.joinpath("datafile_invalid_type.json")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--load-data", str(data_file), str(test_file_src)])

            assert "must be a top level dictionary/hash" in str(excinfo.value), "Exception raised is incorrect"
