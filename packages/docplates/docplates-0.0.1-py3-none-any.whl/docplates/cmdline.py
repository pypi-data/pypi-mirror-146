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

"""Entry point into Docplates from the commandl ine."""

import argparse
import datetime
import json
import logging
import logging.handlers
import os.path
import pathlib
import sys
from typing import Any, Dict, List, NoReturn, Optional, Tuple

import jinja2.exceptions
import yaml
import yaml.parser
import yaml.scanner

from .docplates import Docplates
from .exceptions import DocplatesError, DocplatesUsageError
from .version import __version__

__all__ = [
    "DocplatesArgumentParser",
    "DocplatesCommandLine",
]


CONFIG_FILE = "~/.config/docplates.conf"


class DocplatesArgumentParser(argparse.ArgumentParser):
    """ArgumentParser override class to output errors slightly better."""

    def error(self, message: str) -> NoReturn:
        """
        Slightly better error message handler for ArgumentParser.

        Parameters
        ----------
        message : :class:`str`
            Error message.

        """
        raise DocplatesUsageError(message, self)


class DocplatesCommandLine:
    """
    Docplates command line handling class.

    This class takes no arguments during instantiation.
    """

    _args: argparse.Namespace
    _argparser: DocplatesArgumentParser

    def __init__(self) -> None:
        """
        Docplates command line handling class.

        This class takes no arguments during instantiation.
        """

        self._args = argparse.Namespace()
        self._argparser = DocplatesArgumentParser(add_help=False)

    def run(  # pylint: disable=too-many-branches,too-many-locals,too-many-statements  # noqa: C901,CFQ001
        self,
        args: Optional[List[str]] = None,
        setup_console_logging: bool = False,
        is_api: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Run Docplates using command line arguments.

        This can also be called via an API, passing the args as the command line arguments.

        Parameters
        ----------
        args : :class:`Optional` [ :class:`List` [ :class:`str` ] ]
            Commandline arguments to pass.

        setup_console_logging : :class:`bool`
            Setup console logging, this can be used if logging is not already setup and configured. The purpose of this option
            is to setup the Python logging module with relatively sane defaults.

        is_api : :class:`bool`
            Indicate that this is an API call and normal output to the terminal shouldn't take place. Defaults to True.

        Returns
        -------
        :class:`Optional` [ :class:`Dict` [ :class:`str` , :class:`Any` ]] :
            Exported variables from template.

        """

        # Add docplates arguments
        docplates_group = self.argparser.add_argument_group("Docplates arguments")
        docplates_group.add_argument("-h", "--help", action="help", help="Show this help message and exit.")
        docplates_group.add_argument("-v", "--verbose", action="store_true", help="Display verbose logging.")
        docplates_group.add_argument(
            "-c",
            "--config-file",
            nargs=1,
            metavar="CONFIG_FILE",
            default=[CONFIG_FILE],
            help=f"Config file to use (default: {CONFIG_FILE}).",
        )
        # Input file
        docplates_group.add_argument(
            "input_file",
            metavar="INPUT_FILE",
            nargs="?",
            help="Docplates template file to process.",
        )

        # Data source arguments
        data_source_group = self.argparser.add_argument_group("Data source arguments")
        # Set a variable
        data_source_group.add_argument(
            "-l",
            "--load-data",
            metavar="DATA_FILE",
            default=[],
            action="append",
            help="This option will parse a number of DATA_FILE's with .yaml or .json file extensions and load the data into the "
            "'data' global.",
        )
        # Set a variable
        data_source_group.add_argument(
            "-s",
            "--set",
            metavar="KEY=VALUE",
            action="append",
            help="Set a number of key-value pairs to be passed to the template environment in the 'data' global, these will "
            "override those loaded from a data file. This option can be specified multiple times. Instead of the = a += can be "
            "provided which will have the effect of creating a list value.",
        )

        # Data source arguments
        output_pdf_group = self.argparser.add_argument_group("Output PDF arguments")
        # Output file
        output_pdf_group.add_argument(
            "-o",
            "--output-file",
            metavar="OUTPUT_FILE",
            help="Specify the output filename.",
        )
        # Disable PDF encryption
        output_pdf_group.add_argument(
            "--no-encryption",
            default=False,
            action="store_true",
            help="Disable PDF encryption. By default all generated PDF's are encrypted.",
        )
        # Disable output subdirectory
        output_pdf_group.add_argument(
            "--no-subdir",
            default=False,
            action="store_true",
            help="Disable placing the resulting default output file in a subdirectory.",
        )
        # Disable output filename timestamping
        output_pdf_group.add_argument(
            "--no-timestamp",
            default=False,
            action="store_true",
            help="Disable adding a timestamp to the default output filename.",
        )

        # Data export arguments
        export_group = self.argparser.add_argument_group("Data export arguments")
        export_group.add_argument(
            "--export",
            nargs="?",
            const=True,
            action="store",
            help="File to write export data to, either a file path or '-' for stdout. Defaults to the output filename with a json"
            " extension.",
        )
        export_group.add_argument(
            "--export-format",
            nargs=1,
            default=None,
            choices=["json", "yaml"],
            help="Format of the export data, either 'json' or 'yaml' (default: json).",
        )

        # Debugging and troubleshooting arguments
        debug_group = self.argparser.add_argument_group("Debugging and troubleshooting arguments")
        debug_group.add_argument(
            "--preserve-build",
            action="store_true",
            default=False,
            help="Preserve build files, by default in a build/ or .build directory.",
        )
        debug_group.add_argument("--list-modules", action="store_true", help="List Python modules loaded.")
        debug_group.add_argument("--list-plugins", action="store_true", help="List plugins loaded.")
        debug_group.add_argument("--list-template-search-paths", action="store_true", help="List template search paths.")

        # Parse command line args
        self._args = self.argparser.parse_args(args)

        # Setup logging
        if setup_console_logging:
            self._setup_console_logging()

        # Check for invalid combination of output_file and no_timestamp/no_subdir
        if self.args.output_file and (self.args.no_timestamp or self.args.no_subdir):
            raise DocplatesUsageError(
                "Using --output-file and --no-timestamp or --no-subdir is pointless to use at the same time",
                self.argparser,
            )

        # Check for invalid use of --export-format without --export
        if self.args.export_format and not self.args.export:
            raise DocplatesUsageError("Using --export-format without --export makes no sense", self.argparser)

        # Load config
        config_filename = self.args.config_file[0]
        # Expand path if it contains a user home directory
        config_filename_expanded = os.path.expanduser(self.args.config_file[0])
        # Load configuration
        config = {}
        # If the file exists or if the user has specified the config file, then we continue
        # NK: this will result in a non-existent specified config file generating an error rather than being ignored
        if os.path.exists(config_filename_expanded) or config_filename != CONFIG_FILE:
            # Try load config file
            try:
                with open(config_filename_expanded, "r", encoding="UTF-8") as config_file:
                    loaded_config = yaml.safe_load(config_file)
                    # Only replace our config if we actually loaded configuration
                    # NK: This prevents a NoneType error and an additional IF to set the config to {} if its empty
                    if loaded_config:
                        config = loaded_config
            except (yaml.YAMLError, OSError) as exc:
                raise DocplatesError(f"Failed to load configuration from '{config_filename}': {exc}") from None

        # Check what we're going to be doing
        if self.args.list_modules or self.args.list_plugins or self.args.list_template_search_paths:
            return self._output_debug_info(config, is_api)

        if not self.args.input_file:
            raise DocplatesUsageError("Nothing to do, invalid invocation arguments", self.argparser)

        # Grab our exports
        output_file, exports = self._generate_pdf(config)

        # No request was given to export data, so we just return the exports here
        if self.args.export is not None:
            self._export_data(exports, output_file)

        return exports

    def _export_data(self, exports: Optional[Dict[str, Any]], output_file: pathlib.Path) -> None:
        """
        Export data we got from the template.

        Parameters
        ----------
        exports : class:`Optional` [ :class:`Dict` [ class:`str`, :class:`Any` ] ]
            Data to export that we got from the template.

        output_file: :class:`pathlib.Path`
            File that the PDF was written to.

        """

        # Check for default...
        if self.args.export_format is None:
            export_format = "json"
        else:
            export_format = self.args.export_format[0]

        # Create export data
        export_data = ""
        if export_format == "json":
            export_data = json.dumps(exports)
        elif export_format == "yaml":
            export_data = yaml.safe_dump(exports)

        # Work out a possible export filename
        if self.args.export is True:
            export_destination = output_file.with_suffix(f".{export_format}")

        # Check if we're writing to stdout
        elif self.args.export == "-":
            # If we are, write it out
            print(export_data)
            return

        # If we made it here, it is some other string .... most notably a filename
        else:
            export_destination = self.args.export

        # If not stdout, it's going to be a file
        try:
            export_path = pathlib.Path(export_destination).expanduser()
            export_path.write_text(export_data, encoding="UTF-8")
            logging.info("Docplates: Wrote export data to '%s'", export_path)
        except OSError as exc:
            raise DocplatesError(f"Failed to write file '{export_destination}': {exc}") from None

    def _output_debug_info(self, config: Any, is_api: bool) -> Dict[str, Any]:
        """
        Output debug info.

        Parameters
        ----------
        config : :class:`Any`
            Configuration data pulled from config file.

        is_api : :class:`bool`
            Indicates this is an API call and normal console output shouldn't take place.

        """

        # Create docplates object
        docplates = Docplates(config=config)

        # Save a copy of the output to return
        output: Dict[str, Any] = {}

        if self.args.list_modules:
            if not is_api:
                logging.info("Docplates: Python Modules Loaded")
            output["modules"] = []
            for module in sorted(sys.modules.copy().keys()):
                if not is_api:
                    logging.info("Docplates:  - %s", module)
                output["modules"].append(module)

        if self.args.list_plugins:
            if not is_api:
                logging.info("Docplates: Docplates Plugins Loaded")
            output["plugins"] = []
            for plugin in docplates.plugin_manager.modules:
                if not is_api:
                    logging.info("Docplates:  - %s", plugin.module_name)
                output["plugins"].append(plugin.module_name)

        if self.args.list_template_search_paths:
            if not is_api:
                logging.info("Docplates: Docplates Template Search Paths")
            output["template_search_paths"] = []
            for search_path in docplates.template_search_paths:
                if not is_api:
                    logging.info("Docplates:  - %s", search_path)
                output["template_search_paths"].append(search_path)

        return output

    def _generate_pdf(  # pylint: disable=too-many-branches, too-many-statements # noqa: CFQ001,CFQ004,C901
        self, config: Any
    ) -> Tuple[pathlib.Path, Optional[Dict[str, Any]]]:
        """
        Generate PDF.

        Parameters
        ----------
        config : :class:`Any`
            Configuration data pulled from config file.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Any` ] :
            Variables exported from template.

        """

        # Grab template variables
        template_variables = self._get_variables()

        # Create docplates object
        docplates = Docplates(config=config)

        # This determines if we're copying the source directory somewhere
        copy_source_to: Optional[pathlib.Path] = None

        # Workout input and output filenames
        input_file = pathlib.Path(self.args.input_file).expanduser()
        if not input_file.is_file():
            raise DocplatesError(f"Failed to locate input file '{self.args.input_file}'")
        # Check if we were provided and output file
        if self.args.output_file:
            output_file = pathlib.Path(self.args.output_file).expanduser()
            if self.args.preserve_build:
                copy_source_to = pathlib.Path(f"{output_file}.build")
        else:
            # If not use the INPUT_FILE.pdf by d efault
            output_file = input_file.with_suffix(".pdf")
            output_name = output_file.stem
            # Check if we're doing timestamping on the output filename
            if not self.args.no_timestamp:
                # Work out the timestamp from the modification date of the file
                timestamp = datetime.datetime.fromtimestamp(input_file.stat().st_mtime).strftime(r"%Y%m%d%H%M")
                # Work out the output name to use
                output_name = f"{output_file.stem} - {timestamp}"
            # Check if we're going to use a sub directory or not
            if not self.args.no_subdir:
                output_file = output_file.parent.joinpath(output_name).joinpath(f"{output_name}{output_file.suffix}")
            else:
                output_file = output_file.parent.joinpath(f"{output_name}{output_file.suffix}")
                logging.debug("Docplates: Using timestamped output filename '%s'", output_file)
            # Now for the preserve build stuff, if we're preserving the build
            if self.args.preserve_build:
                # And we are using a subdir...
                if not self.args.no_subdir:
                    # Then just add /build to the end
                    copy_source_to = output_file.parent.joinpath("build")
                # Else use .build
                else:
                    copy_source_to = pathlib.Path(f"{output_file}.build")

        # If we're copying the source somewhere, just output a bit of debug about that
        if copy_source_to:
            logging.debug("Docplates: Preserving build files in '%s'", copy_source_to)

        # Load template and get exports
        exports = docplates.generate(
            input_file=input_file,
            output_file=output_file,
            variables=template_variables,
            encrypt=not self.args.no_encryption,
            copy_source_to=copy_source_to,
        )

        return output_file, exports

    def _get_variables(self) -> Dict[str, Any]:  # pylint: disable=too-many-branches
        """
        Load data from key-value pairs on the command line and datafiles.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Any` ] :
            Dictionary of strings and any value.

        """

        template_variables: Dict[str, Any] = {}

        # Loop with data files
        for data_filename in self.args.load_data:
            # Resolve path
            data_filename_path = pathlib.Path(data_filename).expanduser()
            # Make sure file exists
            if not data_filename_path.is_file():
                raise DocplatesError(f"Data file does not exist: {data_filename}")

            # Check what type the file is and load it
            data: Any = None
            # JSON files
            if data_filename_path.suffix == ".json":
                try:
                    data = json.loads(data_filename_path.read_bytes())
                except json.decoder.JSONDecodeError as exc:
                    raise DocplatesError(f"Error loading JSON data file '{data_filename}': {exc}") from None
            # YAML files
            elif data_filename_path.suffix == ".yaml":
                try:
                    data = yaml.safe_load(data_filename_path.read_bytes())
                except (yaml.scanner.ScannerError, yaml.parser.ParserError) as exc:
                    raise DocplatesError(f"Error loading YAML data file '{data_filename}': {exc}") from None
            else:
                raise DocplatesError(f"Data file '{data_filename}' has unsupported extension (use .json or .yaml)")
            # Make sure its a dict we got
            if not isinstance(data, dict):
                raise DocplatesError(f"Data file '{data_filename}' must be a top level dictionary/hash")

            # Update template variables
            template_variables.update(data)
            logging.info(
                "Docplates: Loaded data file: %s (%s variables, %s total)", data_filename, len(data), len(template_variables)
            )

        # Work out variables to pass
        if self.args.set:
            for set_item in self.args.set:
                (set_key, set_value) = (str(x) for x in set_item.split("=", 1))
                # Check if this is an add action
                add_value = False
                if set_key.endswith("+"):
                    # Strip the +
                    set_key = set_key.rstrip("+")
                    add_value = True
                # If the key exists and we're adding, we must setup a list
                if set_key in template_variables and add_value:
                    # We save the current value to make linting happy
                    cur_value = template_variables[set_key]
                    if isinstance(cur_value, str):
                        cur_value = [cur_value]
                        cur_value.append(set_value)
                    else:
                        cur_value.append(set_value)
                    # Set the template variable value now for the key
                    template_variables[set_key] = cur_value
                    logging.info("Docplates: Data added to variable '%s' (%s total variables)", set_key, len(template_variables))
                # If we don't have a value, we need to treat add_value specially
                elif add_value:
                    template_variables[set_key] = [set_value]
                    logging.info("Docplates: Data list variable '%s' set (%s total variables)", set_key, len(template_variables))
                # Item doesn't exist, so we can just add it
                else:
                    template_variables[set_key] = set_value
                    logging.info("Docplates: Data variable '%s' set (%s total variables)", set_key, len(template_variables))

        return template_variables

    def _setup_console_logging(self) -> None:
        """Set up console logging."""

        # Setup logger and level
        logger = logging.getLogger()
        if self.args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        # Setup console handler
        console_handler = logging.StreamHandler()
        # Use a better format for messages
        console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
        logger.addHandler(console_handler)

    @property
    def args(self) -> argparse.Namespace:
        """
        Commandline arguments.

        Returns
        -------
        :class:`~argparse.Namespace` :
            Parsed command line arguments.

        """
        return self._args

    @property
    def argparser(self) -> argparse.ArgumentParser:
        """
        Return our ArgumentParser instance.

        Returns
        -------
        :class:`~argparse.ArgumentParser` :
            Commandline argument parser.

        """
        return self._argparser


# NK: This is our command line entry point
def main(args: Optional[List[str]] = None) -> int:  # noqa: CFQ004  # pragma: no cover
    """Run Docplates."""
    try:
        print(f"Docplates v{__version__} - Copyright © 2015-2022, AllWorldIT.\n", file=sys.stderr)
        docplates_cmdline = DocplatesCommandLine()
        docplates_cmdline.run(args=args, setup_console_logging=True, is_api=False)
    except DocplatesError as exception:
        print(f"ERROR: {exception}", file=sys.stderr)
        return 1
    except DocplatesUsageError as exception:
        print(f"USAGE ERROR: {exception}", file=sys.stderr)
        return 2
    except jinja2.exceptions.TemplateError as exception:
        print(f"TEMPLATE ERROR: {exception}", file=sys.stderr)
        return 3
    return 0
