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

"""Docplates tests."""

import os
import pathlib
import shutil
import tempfile
from typing import List

import jinja2.exceptions
import markupsafe
import pytest

import docplates

from ..base import BaseTest

__all__: List[str] = []


class TestDocplates(BaseTest):
    """Basic test."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Basic test for .tex templates."""

        docp = docplates.Docplates(config={})

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
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Basic test for .html templates."""

        docp = docplates.Docplates(config={})

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
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"


class TestDocplatesEscape(BaseTest):
    """Test escaping of values."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Test escaping of values for .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_escape.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"
            assert exports == {"test_escape": r"\textbackslash\{\}hello\_world"}, "Escaped string is incorrect"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Test escaping of values for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_escape.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            # Generate PDF
            exports = docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"
            assert exports == {"test_escape": markupsafe.Markup.escape("<hello></hello>")}, "Escaped string is incorrect"


class TestDocplatesIncludes(BaseTest):
    """Basic includes test."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Basic includes test for .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include.tex")
        someinclude_file = mydir.joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_include_src = test_dir_path.joinpath("someinclude.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Basic include test for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include.html")
        someinclude_file = mydir.joinpath("someinclude.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_include_src = test_dir_path.joinpath("someinclude.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"


class TestDoubleTemplateIncludes(BaseTest):
    """Double include tests."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Double include test for .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_double.tex")
        someinclude_file = mydir.joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_include_src = test_dir_path.joinpath("someinclude.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Double include test for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_double.html")
        someinclude_file = mydir.joinpath("someinclude.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_include_src = test_dir_path.joinpath("someinclude.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert os.path.isfile(test_file_dst) is True, "PDF file not generated"


class TestTemplateNotFoundException(BaseTest):
    """Test template not found exception."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Test template not found for .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_not_found.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(jinja2.exceptions.TemplateNotFound) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert "include_does_not_exist.tex" in str(excinfo.value), "Exception information is incorrect"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Test template not found for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_not_found.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(jinja2.exceptions.TemplateNotFound) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert "include_does_not_exist.html" in str(excinfo.value), "Exception information is incorrect"


class TestTemplateBadExtensionException(BaseTest):
    """Test template bad extension exception."""

    def test_tex(self) -> None:  # pylint: disable=no-self-use
        """Test template bad extension for .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_bad_extension.tex")
        someinclude_file = mydir.joinpath("someinclude.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_include_src = test_dir_path.joinpath("someinclude.dat")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            with pytest.raises(jinja2.exceptions.TemplateNotFound) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert "someinclude.dat" in str(excinfo.value), "Exception information is incorrect"

    def test_html(self) -> None:  # pylint: disable=no-self-use
        """Test template bad extension for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_include_bad_extension.html")
        someinclude_file = mydir.joinpath("someinclude.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_include_src = test_dir_path.joinpath("someinclude.dat")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)
            shutil.copy(someinclude_file, test_include_src)

            # Generate PDF
            with pytest.raises(jinja2.exceptions.TemplateNotFound) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert "someinclude.dat" in str(excinfo.value), "Exception information is incorrect"


class TestTemplateBrokenTemplatesException(BaseTest):
    """Test broken template exceptions."""

    def test_broken_tex(self) -> None:  # pylint: disable=no-self-use
        """Test broken template .tex templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_broken.tex")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.tex")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            with pytest.raises(docplates.DocplatesError) as excinfo:
                docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            assert "Failed to render PDF document" in str(excinfo.value), "Exception information is incorrect"

    # NK: There is currently no real way to test a broken HTML file sadly, WeasyPrint ignores exceptions
    # NK: We keep this around however to test the output message code
    def test_broken_html(self) -> None:  # pylint: disable=no-self-use
        """Test broken template for .html templates."""

        docp = docplates.Docplates(config={})

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_broken.html")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_file_src = test_dir_path.joinpath("helloworld.html")
            test_file_dst = test_dir_path.joinpath("helloworld.pdf")

            # Copy source file
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF
            # with pytest.raises(docplates.DocplatesError) as excinfo:
            docp.generate(input_file=test_file_src, output_file=test_file_dst, variables={})

            # assert "Failed to render PDF document" in str(excinfo.value), "Exception information is incorrect"


class TestWeasyPrintLinkOutOfPathFile(BaseTest):
    """Test file attempted to be linked in WeasyPrint that is out of path."""

    def test_link_resolves_to_wrong_dir(self) -> None:  # pylint: disable=no-self-use
        """Test file attempted to be linked in WeasyPrint that is out of path."""

        docp_commandline = docplates.DocplatesCommandLine()

        mydir = pathlib.Path(os.path.dirname(__file__))
        helloworld_file = mydir.joinpath("helloworld_resource_out_of_path.html")
        image_file = mydir.joinpath("image.png")

        with tempfile.TemporaryDirectory(prefix="docplates-test") as test_dir:
            # Work out destination paths
            test_dir_path = pathlib.Path(test_dir)
            test_dir_path_subdir = test_dir_path.joinpath("basedir")
            image_file_dst = test_dir_path.joinpath("image.png")
            test_file_src = test_dir_path_subdir.joinpath("helloworld.html")
            test_file_dst = test_dir_path_subdir.joinpath("helloworld.pdf")

            # Copy source file
            test_dir_path_subdir.mkdir()
            shutil.copy(image_file, image_file_dst)
            shutil.copy(helloworld_file, test_file_src)

            # Generate PDF

            # NK: We're testing the code coverage with this, as WeasyPrint ignores exceptions, we not going to get much back
            # with pytest.raises(docplates.DocplatesError) as excinfo:
            docp_commandline.run(["--output", str(test_file_dst), str(test_file_src)])

        # assert "Resource 'image_not_exist.png' not found" in str(excinfo.value), "Exception information is incorrect"
