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

"""Docplates command line config file tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import pytest

import docplates

from ...base import BaseTest

__all__: List[str] = []


class TestConfigFile(BaseTest):
    """Docplates command line config file test."""

    def test_config_file_blank(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file is blank."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        config_file = mydir.joinpath("blank.conf")

        docp_commandline.run(["--config", str(config_file), "--list-plugins"])

    def test_config_file_valid(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file is blank."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        config_file = mydir.joinpath("valid.conf")

        docp_commandline.run(["--config", str(config_file), "--list-plugins"])

    def test_config_file_not_exist(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file does not exist."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        config_file = mydir.joinpath("config.does.not.exist.conf")

        with pytest.raises(docplates.DocplatesError) as excinfo:
            docp_commandline.run(["--config", str(config_file), "--list-plugins"])

        assert "No such file or directory" in str(excinfo.value), "Exception information is incorrect"

    def test_config_file_invalid(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file is invalid."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        config_file = mydir.joinpath("invalid.conf")

        with pytest.raises(docplates.DocplatesError) as excinfo:
            docp_commandline.run(["--config", str(config_file), "--list-plugins"])

        assert "Failed to load configuration" in str(excinfo.value), "Exception information is incorrect"


class TestConfigFileExceptions(BaseTest):
    """Docplates command line config file exceptions test."""

    def test_invalid_addon_paths_config_type_path(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file has invalid addon_paths."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            test_config_file = test_dir_path.joinpath("invalid_addon_paths_config_type.tex")
            invalid_addon_paths_config_type = test_dir_path.joinpath("non_existing_template_search_path")

            test_config_file.write_text(f"addon_paths:\n  wrong:\n    - {invalid_addon_paths_config_type}", encoding="UTF-8")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--config-file", str(test_config_file), str(test_file_src)])

        assert "Configuration option 'addon_paths' must be a list" in str(excinfo.value), "Exception raised is incorrect"

    def test_invalid_template_search_paths_config_type_path(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file has invalid template_search_paths."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            test_config_file = test_dir_path.joinpath("invalid_template_search_paths_config_type.tex")
            invalid_template_search_paths_config_type = test_dir_path.joinpath("non_existing_template_search_path")

            test_config_file.write_text(
                f"template_search_paths:\n  wrong:\n    - {invalid_template_search_paths_config_type}", encoding="UTF-8"
            )

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--config-file", str(test_config_file), str(test_file_src)])

        assert "Configuration option 'template_search_paths' must be a list" in str(excinfo.value), "Exception raised is incorrect"

    def test_non_existing_template_search_path(self) -> None:  # pylint: disable=no-self-use
        """Test command line when config file has invalid template_search_path."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.parent.joinpath("helloworld.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")

            test_config_file = test_dir_path.joinpath("non_existing_template_search_path.tex")
            non_existing_template_search_path = test_dir_path.joinpath("non_existing_template_search_path")

            test_config_file.write_text(f"template_search_paths:\n  - {non_existing_template_search_path}", encoding="UTF-8")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp_commandline.run(["--config-file", str(test_config_file), str(test_file_src)])

        assert f"Template search path '{non_existing_template_search_path}/templates' is not a directory or cannot be found" in str(
            excinfo.value
        ), "Exception raised is incorrect"
