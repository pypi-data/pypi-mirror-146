#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2015-2022, AllWorldIT.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Docplates LaTeX backend."""

import logging
import os
import pathlib
import re
import subprocess  # nosec
from typing import Callable, Dict, List, Optional, Tuple, Union

import ezplugins
import markupsafe

from ...exceptions import DocplatesError
from . import DocplatesBackend

__all__: List[str] = []


class DocplatesLatexBackend(DocplatesBackend):
    """Docplates LaTeX backend class."""

    def __init__(self) -> None:
        """Initialize object."""
        super().__init__()

        # Setup our backend attributes
        self._template_extensions = ["tex"]
        self._resource_extensions = ["pdf", "png"]
        self._jinja_environment_options = {
            "block_start_string": r"\BLOCK{",
            "block_end_string": r"}",
            "variable_start_string": r"\VAR{",
            "variable_end_string": r"}",
            "comment_start_string": r"\#{",
            "comment_end_string": r"}",
            "line_statement_prefix": r"%%",
            "line_comment_prefix": r"%#",
        }

    def render(self, template_file_path: pathlib.Path) -> pathlib.Path:
        """
        Render the template file.

        Parameters
        ----------
        template_file_path : :class:`pathlib.path`
            Template file path to render.

        Returns
        -------
        :class:`pathlib.Path` :
            Rendered file's path.

        """

        logging.info("LaTeX Backend: Generating PDF...")

        # Render the templated file
        render_results = self._latex(template_file_path)
        if not render_results:
            raise DocplatesError("Failed to render PDF document")

        # Grab results
        (rendered_file_path, page_count) = render_results
        # logging.info("LaTeX Backend: Wrote %s pages to '%s'", page_count, rendered_file_path)
        logging.info("LaTeX Backend: Generated %s page(s)", page_count)

        return rendered_file_path

    def _latex(self, filename: pathlib.Path) -> Optional[Tuple[pathlib.Path, int]]:  # pylint: disable=no-self-use
        """
        Run the LaTeX command.

        Parameters
        ----------
        filename : :class:`pathlib.Path`
            Tex filename to run LaTeX on.

        Returns
        -------
        :class:`Optional` [ :class:`Tuple` [ :class:`str`, :class:`int` ] ] :
            A (rendered_filename, page_count) tuple if the command succeeded.

        """

        # Latex command to run
        latex_command = [
            "latexmk",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-norc",
            "-verbose",
            "-Werror",
            "-pdf",
        ]

        # ENV to pass to command
        env = os.environ.copy()
        env["max_print_line"] = "9999"

        # Add output directory to command
        latex_command.append(f"-output-directory={filename.parent}")
        # Add filename to render
        latex_command.append(str(filename))

        # Keep the log of output incase we get an error
        latex_log = []

        # We will track the rendered filename and the page count
        rendered_filename: Optional[pathlib.Path] = None
        page_count: Optional[int] = None

        process = subprocess.Popen(  # pylint: disable=consider-using-with # nosec
            latex_command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # NK: Probably not easy to reach under any normal circumstances
        if not process.stdout:  # pragma: no cover
            raise DocplatesError("Failed to spawn LaTeX subprocess")
        while True:
            raw_line = process.stdout.readline()
            if process.poll() is not None and raw_line == b"":
                break
            if raw_line:
                line = raw_line.decode("UTF-8").strip()
                logging.debug("LaTeX Backend: %s", line)
                latex_log.append(line)
                # Lets see if we can get the output filename
                matches = re.match(r"Output written on (?P<rendered_filename>.+) \((?P<page_count>\d+) page", line)
                if matches:
                    rendered_filename = pathlib.Path(matches.group("rendered_filename"))
                    page_count = int(matches.group("page_count"))

        retval = process.poll()
        if retval:
            # Output the latex log if we got a non-zero exit status
            for line in latex_log:
                logging.warning(line)
            # Output the return value with an error logging message
            logging.error("LaTeX Backend: LaTeX return status %s", retval)
            return None

        # Make sure we detected the output
        # NK: Probably not reachable under any normal circumstances
        if not rendered_filename or not page_count:  # pragma: no cover
            logging.error("LaTeX Backend: LaTeX return status %s, but there was no output detected", retval)
            return None

        return (rendered_filename, page_count)


def _escape_tex(text: Union[str, markupsafe.Markup]) -> Union[str, markupsafe.Markup]:
    """
    Escape a tex string.

    Parameters
    ----------
    text : :class:`str`
        Text to escape.

    Returns
    -------
    :class:`str` :
        Escaped tex string.

    """
    conv = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "<": r"\textless{}",
        ">": r"\textgreater{}",
    }

    # NK: This is probably not reachable, and would be already-escaped HTML
    if isinstance(text, markupsafe.Markup):  # pragma: no cover
        # Return value
        text = text.unescape()

    # Do tex conversion replacements
    text = str(text)

    for char, char_replace in conv.items():
        text = text.replace(char, char_replace)

    return text


@ezplugins.ezplugin
class DocplatesLatexBackendPlugin:
    """Docplates LaTex backend class."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_backend(self, template_file: str) -> Optional[DocplatesBackend]:  # pylint: disable=no-self-use
        """
        Return the backend if we can handle the filename provided.

        Returns
        -------
        :class:`Optional` [ :class:`DocplatesBackend` ] :
            A DocplatesBackend if it supports this template filename.

        """

        if template_file.endswith(".tex"):
            return DocplatesLatexBackend()

        return None

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_filters(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., str]]:
        """
        Return the filters for this backend.

        Parameters
        ----------
        backend : :class:`DocplatesBackend`
            Backend that is currently being used.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Callable` [ ..., :class:`str` ] ] :
            Dict of filter callables indexed by the filter name.

        """

        filters: Dict[str, Callable[..., str]] = {}

        # If this is our latex backend, then load the safe filter
        if isinstance(backend, DocplatesLatexBackend):
            filters["escape"] = _escape_tex
            filters["e"] = _escape_tex

        return filters
