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

"""Docplates WeasyPrint backend."""

import logging
import mimetypes
import pathlib
from typing import Any, Callable, Dict, List, Optional, Tuple

import ezplugins
import pydyf
import weasyprint

from ... import __version__ as __docplates_version__
from ...exceptions import DocplatesError, DocplatesResourceNotFoundError
from . import DocplatesBackend

__all__: List[str] = []


class DocplatesWeasyprintBackend(DocplatesBackend):
    """Docplates WeasyPrint backend class."""

    def __init__(self) -> None:
        """Initialize object."""
        super().__init__()

        # Setup our backend attributes
        self._template_extensions = ["html"]
        self._resource_extensions = ["css", "otf", "png", "ttf"]

        # Initialize the mimetypes
        mimetypes.init()

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

        logging.info("WeasyPrint Backend: Generating PDF...")

        # Render the templated file
        render_results = self._weasyprint(template_file_path)
        # NK: Probably not reachable under any normal circumstances
        if not render_results:  # pragma: no cover
            raise DocplatesError("Failed to render PDF document")

        # Grab results
        (rendered_file_path, page_count) = render_results
        # logging.info("WeasyPrint Backend: Wrote %s pages to '%s'", page_count, rendered_file_path)
        logging.info("WeasyPrint Backend: Generated %s page(s)", page_count)

        return rendered_file_path

    def _weasyprint(self, filename: pathlib.Path) -> Optional[Tuple[pathlib.Path, int]]:
        """
        Run WeasyPrint to render the HTML.

        Parameters
        ----------
        filename : :class:`pathlib.Path`
            HTML filename to run WeasyPrint on.

        Returns
        -------
        :class:`Optional` [ :class:`Tuple` [ :class:`str`, :class:`int` ] ] :
            A (rendered_filename, page_count) tuple if the command succeeded.

        """

        page_count = 0

        def pdf_finisher(document: weasyprint.Document, pdf: pydyf.PDF) -> None:  # pylint: disable=unused-argument
            """
            Finisher responsible for changing the PDF before final output.

            Currently we just set the Producer field to ourselves.

            Parameters
            ----------
            document : :class:`weasyprint.Document`
                WeasyPrint document object.

            pdf : :class:`pydyf.PDF`
                Pydyf PDF object.

            """
            nonlocal page_count

            pdf.info["Producer"] = pydyf.String(f"Docplates v{__docplates_version__}")
            page_count = pdf.pages["Count"]

        output_filename = filename.with_suffix(".pdf")

        # Start up WeasyPrint
        htmldoc = weasyprint.HTML(
            filename=filename,
            base_url=f"file://{filename}",
            # Pass the url and parent directory to the fetcher
            url_fetcher=lambda url: self._url_fetcher(url, filename.parent),
        )

        # Render the document and write out the PDF
        htmldoc.render().write_pdf(target=output_filename, finisher=pdf_finisher)

        # Return the rendered filename and page count
        return (output_filename, page_count)

    def _url_fetcher(self, url: str, directory: pathlib.Path) -> Dict[str, Any]:  # pylint: disable=no-self-use
        """
        Fetch a URL and use the directory to make sure that's where it is.

        Parameters
        ----------
        url : :class:`str`
            URL of file to fetch.

        directory : :class:`pathlib.Path`
            Base directory of where the files are.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Any` ] :
            Return the results in a dictionary that WeasyPrint understands.

        """
        if not url.startswith("file://"):
            raise DocplatesResourceNotFoundError("Only resources loaded locally are supported")

        # Strip off file:// which is 7 characters long
        filename = pathlib.Path().joinpath(url[7:]).resolve()
        filename_str = str(filename)

        # Make sure the filename starts with the directory it is in
        if not filename_str.startswith(str(directory)):
            raise DocplatesResourceNotFoundError(
                f"Resource '{url}' => '{filename}' doesn't seem to point to the correct location '{directory}'"
            )

        # Try work out mimetype
        # NK: This is not easily possible to test, if not impossible as the file extensions we allow have a fallback mimetype
        # NK: without testing content. There is no way to override the backend before document creation as the environment is
        # NK: created before control is passed to the backend, and the backend is the one that sets up the permitted extensions.
        mimetype = mimetypes.guess_type(url)[0]
        if not mimetype:  # pragma: no cover
            raise DocplatesResourceNotFoundError(f"Resource '{url}' cannot be resolved to a mime type")

        logging.debug("WeasyPrint Backend: URL fetched '%s' from '%s' with mime-type '%s'", filename, url, mimetype)

        # Return the file contents
        return {"string": filename.read_bytes(), "mime_type": mimetype}


@ezplugins.ezplugin
class DocplatesWeasyPrintBackendPlugin:
    """Docplates WeasyPrint backend class."""

    def __init__(self) -> None:
        """Initialize object."""

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_backend(self, template_file: str) -> Optional[DocplatesBackend]:  # pylint: disable=no-self-use
        """
        Return the backend if we can handle the filename provided.

        Returns
        -------
        :class:`Optional` [ :class:`DocplatesBackend` ] :
            A DocplatesBackend if it supports this template filename.

        """

        if template_file.endswith(".html"):
            return DocplatesWeasyprintBackend()

        return None

    @ezplugins.ezplugin_method()  # type: ignore
    def docplates_get_filters(  # pylint: disable=unused-argument,no-self-use
        self, backend: DocplatesBackend
    ) -> Dict[str, Callable[..., str]]:
        """
        Return the filters for this backend.

        Returns
        -------
        :class:`Dict` [ str, :class:`Callable` [ ..., :class:`str` ] ] :
            Dict of filter callables indexed by the filter name to be made available in LaTex.

        """

        filters: Dict[str, Callable[..., str]] = {}

        # Escaping of HTML is default in jinja2, we don't need to replace it

        return filters
