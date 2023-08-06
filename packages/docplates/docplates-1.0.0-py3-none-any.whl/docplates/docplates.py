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

"""Docplates package, responsible for rendering of template files into PDF documents."""

import contextlib
import datetime
import logging
import pathlib
import random
import shutil
import string
import sys
import tempfile
import zipfile
from typing import Any, Callable, Dict, List, Optional

import ezplugins
import jinja2
import jinja2.ext
import jinja2.lexer
import jinja2.sandbox
import jinja2.utils
import pikepdf

from .exceptions import DocplatesError, DocplatesResourceNotFoundError
from .loaders import DocplatesFilesystemLoader, DocplatesLoader, DocplatesLoaderResource, DocplatesPluginLoader
from .plugins.backends import DocplatesBackend
from .utils import format_timedelta
from .version import __version__

__all__ = [
    "Docplates",
]


class Docplates:  # pylint: disable=too-few-public-methods
    """
    Docplates object used to parse templates.

    Parameters
    ----------
    config : :class:`Dict` [ :class:`str`, :class:`str` ]
        Dictionary of configuration options, supported options can be found below:

        template_search_paths : :class:`List` [ :class:`str` ]
            List of template search paths, ``~`` is supported to designate the home directory. If the last component (directory) of
            the path is not ``templates``, then it will be appended. For instance ``/home/user/Docplates/mytemplates`` becomes
            ``/home/user/Docplates/mytemplates/templates``. This is to ensure templates are only loaded from ``templates``
            directories.

    plugin_manager : :class:`Optional` [ :class:`~ezplugins.EZPluginManager` ]
        Optional plugin manager to use for loading plugins.

    """

    _config: Dict[str, Any]
    _plugin_manager: ezplugins.EZPluginManager
    _template_backend: Optional[DocplatesBackend]
    _template_filters: Dict[str, Callable[..., str]]
    _template_globals: Dict[str, Any]
    _template_search_paths: List[pathlib.Path]
    _exports: Dict[str, Any]

    def __init__(
        self,
        config: Dict[str, Any],
        plugin_manager: Optional[ezplugins.EZPluginManager] = None,
    ) -> None:
        """
        Docplates object used to parse templates.

        Parameters
        ----------
        config : :class:`Dict` [ :class:`str`, :class:`Any` ]
            Dictionary of configuration options, supported options can be found below:

            template_search_paths : :class:`List` [ :class:`str` ]
                List of template search paths, ``~`` is supported to designate the home directory.

            addon_paths : :class:`List` [ :class:`str` ]
                List of addon search paths, ``~`` is supported to designate the home directory. In addition to specifying directory
                search paths one can also specify a Zip file addon.

        plugin_manager : :class:`Optional` [ :class:`~ezplugins.EZPluginManager` ]
            Optional plugin manager to use for loading plugins.

        """

        self._config = config

        # Check if we were provided with a plugin manager, if so use it, else create our own
        if plugin_manager:
            self._plugin_manager = plugin_manager
        else:
            self._plugin_manager = ezplugins.EZPluginManager()

        # Load our plugins/addons
        self.load_plugins()

        # Initialize plugins which have a docplates_init method
        with contextlib.suppress(ezplugins.EZPluginMethodNotFoundError):
            for plugin_method, plugin in self.plugin_manager.methods(where_name="docplates_init"):
                logging.debug("Docplates:   - Initializing plugin: %s", plugin.fqn)
                plugin_method.run(self.plugin_manager)

        # Work out what search paths we have
        self._template_search_paths = []
        if "template_search_paths" in self._config:
            if not isinstance(self._config["template_search_paths"], list):
                raise DocplatesError("Configuration option 'template_search_paths' must be a list")
            for template_search_path_str in self._config["template_search_paths"]:
                template_search_path = pathlib.Path(template_search_path_str).expanduser()
                # Check if the directory ends in templates/, it must
                if template_search_path.parts[-1] != "templates":
                    template_search_path = template_search_path.joinpath("templates")
                # Check it is indeed a directory
                if not template_search_path.is_dir():
                    raise DocplatesError(f"Template search path '{template_search_path}' is not a directory or cannot be found")
                # If we got this far, its time to append
                self._template_search_paths.append(template_search_path.resolve(strict=True))

        # Intialize
        self._initialize()

    def generate(  # pylint: disable=too-many-locals,too-many-arguments,too-many-branches,too-many-statements # noqa: CFQ001
        self,
        input_file: pathlib.Path,
        output_file: pathlib.Path,
        variables: Dict[str, Any],
        encrypt: bool = True,
        copy_source_to: Optional[pathlib.Path] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Generate document from a template source file.

        Parameters
        ----------
        input_file : :class:`pathlib.Path`
            Input template file.

        output_file : :class:`pathlib.Path`
            Output PDF file.

        variables : :class:`Dict` [ :class:`str`, :class:`Any` ]
            Variables to pass to the template.

        encrypt : :class:`bool`
            Encrypt PDF, defaults to `True`. A random string is used for encryption, which prevents the changing on all non-form
            data.

        copy_source_to : :class:`Optional` [ :class:`~pathlib.Path` ]
            Optional path to copy the sources to.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Any` ] :
            Variables exported from template.

        """

        # Make sure we have the parameters we need
        if not input_file.is_file():
            raise DocplatesError(f"Failed to locate input file '{input_file}'")

        # Get backend responsible for the the template...
        with contextlib.suppress(ezplugins.EZPluginMethodNotFoundError):
            for plugin_method, _ in self.plugin_manager.methods(where_name="docplates_get_backend"):
                # Try see if this plugin provides a backend
                self._template_backend = plugin_method.run(input_file.name)
                # If so, we found what we were looking for
                if self._template_backend:
                    break
        # Check if we have a backend
        if not self._template_backend:
            logging.error("No docplates backends available to handle '%s'", input_file)
            raise DocplatesError(f"No docplates backends available to handle '{input_file}'") from None

        # Time to load the filters
        with contextlib.suppress(ezplugins.EZPluginMethodNotFoundError):
            # Call all the get filters plugins
            for plugin_method, _ in self.plugin_manager.methods(where_name="docplates_get_filters"):
                # Pass the backend we're going to be using
                plugin_filters = plugin_method.run(self._template_backend)
                if plugin_filters:
                    self._template_filters.update(plugin_filters)

        # Time to load the globals
        with contextlib.suppress(ezplugins.EZPluginMethodNotFoundError):
            # Call all the get filters plugins
            for plugin_method, _ in self.plugin_manager.methods(where_name="docplates_get_globals"):
                # Pass the backend we're going to be using
                plugin_globals = plugin_method.run(self._template_backend)
                if plugin_globals:
                    self._template_globals.update(plugin_globals)

        # Create template environment
        template_env = self._create_template_environment(
            template_paths=[input_file.parent, *self._template_search_paths],
            variables={
                "data": variables,
                "DOCUMENT_NAME": output_file.stem,
            },
        )

        # Check if we can get the template
        template = template_env.get_template(input_file.name)

        # Then render it...
        template_render_start_time = datetime.datetime.utcnow()
        template_output = template.render()
        template_render_end_time = datetime.datetime.utcnow()
        # NK: Lets not hide the useful Jinja2 errors we get
        # try:
        #     template_output = template.render()
        # except (jinja2.TemplateSyntaxError) as err:
        #     raise DocplatesError(
        #         f"Failed to render render '{err.name}': {err.message} in template '{err.filename}' line {err.lineno}"
        #     ) from None
        # except (jinja2.TemplateError) as err:
        #     raise DocplatesError(f"Failed to render: {err.message}") from None

        # Work out all resources that were loaded
        resources_loaded: List[DocplatesLoaderResource] = []
        templates_loaded: List[DocplatesLoaderResource] = []
        for loader in getattr(template_env.loader, "loaders", []):
            if isinstance(loader, DocplatesLoader):
                templates_loaded.extend(loader.loaded_templates.values())
                resources_loaded.extend(loader.loaded_resources.values())
        # List the resources and templates as debug info
        logging.debug("Docplates: Templates Loaded")
        for template_loaded in templates_loaded:
            logging.debug("Docplates:  - %s", template_loaded.name)
        logging.debug("Docplates: Resources Loaded")
        for resource_loaded in resources_loaded:
            logging.debug("Docplates:  - %s", resource_loaded.name)

        # Create a temp directory
        with tempfile.TemporaryDirectory(prefix="docplates") as render_dir:
            render_dir_path = pathlib.Path(render_dir)
            logging.debug("Docplates: Using temporary directory '%s'", render_dir_path)

            template_filename = render_dir_path.joinpath(input_file.name)
            logging.debug("Docplates: Wrote template output file '%s'", template_filename)

            # Copy resources into temporary dir
            self._copy_resources(resources=resources_loaded, destination=render_dir_path)

            # Write out templated .tex file
            with template_filename.open("w", encoding="UTF-8") as texfile:
                texfile.write(template_output)

            # Render the resulting PDF
            pdf_render_start_time = datetime.datetime.utcnow()
            rendered_path = self._template_backend.render(template_filename)
            pdf_render_end_time = datetime.datetime.utcnow()

            # Check if the destination directory exists, if not, create it
            output_dir_path = output_file.parent
            if not output_dir_path.is_dir():
                output_dir_path.mkdir()

            # Open the PDF file
            pdf = pikepdf.Pdf.open(rendered_path)  # type: ignore

            # Adjust the metadata
            with pdf.open_metadata(set_pikepdf_as_editor=False) as pdf_metadata:
                pdf_metadata["xmp:CreatorTool"] = f"Docplates {__version__}"
                pdf_metadata["pdf:Producer"] = f"Docplates {__version__}"

            # Check if we should encrypt the resulting PDF
            if encrypt:
                pdf_encrypt_start_time = datetime.datetime.utcnow()
                pdf.save(
                    output_file,
                    encryption=pikepdf.Encryption(  # type: ignore
                        owner="".join(random.choice(string.printable) for i in range(16)),  # nosec
                        user="",
                        allow=pikepdf.Permissions(  # type: ignore
                            modify_annotation=False, modify_assembly=False, modify_other=False
                        ),
                    ),
                )
                pdf_encrypt_end_time = datetime.datetime.utcnow()
                logging.info("Docplates: Wrote PDF to '%s' (ENCRYPTED)", output_file)

                # Work out timing info
                template_render_time = template_render_end_time - template_render_start_time
                pdf_render_time = pdf_render_end_time - pdf_render_start_time
                pdf_encrypt_time = pdf_encrypt_end_time - pdf_encrypt_start_time
                total_time = template_render_time + pdf_render_time + pdf_encrypt_time
                logging.debug(
                    "Timings - Template render: %s, PDF render: %s, Encryption: %s, Total: %s",
                    format_timedelta(template_render_time),
                    format_timedelta(pdf_render_time),
                    format_timedelta(pdf_encrypt_time),
                    format_timedelta(total_time),
                )

            # If not just save it
            else:
                pdf.save(output_file)
                logging.info("Docplates: Wrote PDF to '%s' (NOT ENCRYPTED)", output_file)
                # Work out timing info
                template_render_time = template_render_end_time - template_render_start_time
                pdf_render_time = pdf_render_end_time - pdf_render_start_time
                total_time = template_render_time + pdf_render_time
                logging.debug(
                    "Docplates: Timings => Template render: %s, PDF render: %s, Encryption: -, Total: %s",
                    format_timedelta(template_render_time),
                    format_timedelta(pdf_render_time),
                    format_timedelta(total_time),
                )

            # Check if we're copying the source to somewhere once we're done
            if copy_source_to:
                if copy_source_to.exists():
                    try:
                        shutil.rmtree(copy_source_to)
                    except OSError as exc:
                        logging.warning(
                            "Docplates: Failed to remove destination source directory '%s', source not copied: %s",
                            copy_source_to,
                            exc,
                        )
                # Finally copy
                if not copy_source_to.exists():
                    shutil.copytree(render_dir, copy_source_to)

        return self.exports

    def _initialize(self) -> None:
        """Initialize internals."""

        # We do this before we parse a template
        self._template_backend = None
        self._template_filters = {}
        self._template_globals = {
            "DOCPLATES_VERSION": __version__,
        }
        self._exports = {}

    def load_plugins(self) -> None:  # pylint: disable=too-many-branches
        """Load Docplates plugins and addons."""

        # Load internal plugins
        self.plugin_manager.load_package("docplates.plugins", ignore_errors=True)
        self.plugin_manager.load_modules(r"^docplates_addon_")

        logging.debug("Docplates: Processing plugins...")
        # Make a list of addons to load
        addon_list: Dict[str, str] = {}
        # Extend it if we have additional paths
        if "addon_paths" in self._config:
            if not isinstance(self._config["addon_paths"], list):
                raise DocplatesError("Configuration option 'addon_paths' must be a list")
            for addon_path in self._config["addon_paths"]:
                logging.debug("Docplates:  - Inspecting addon path: %s", addon_path)
                # Expand and absolute the path
                addon_path = pathlib.Path(addon_path).expanduser()

                # Check if the addon is a file, if so its probably a zip file
                if addon_path.is_file():
                    logging.debug("Docplates:    - Addon path is a file, trying to load as Zipfile")
                    # Load file as a zip
                    with zipfile.ZipFile(addon_path) as zip_file:
                        # Loop with zip contents infolist
                        zip_dirs = []
                        for zip_item in zip_file.infolist():
                            if not zip_item.is_dir():
                                logging.debug("Docplates:      - Skipping %s (Not a directory)", zip_item)
                                continue
                            if len(zip_item.filename.split("/")) != 2:  # p
                                logging.debug(
                                    "Docplates:      - Skipping %s (Only looking for component counts of 2, eg. a/b)", zip_item
                                )
                                continue
                            if not zip_item.filename.startswith("docplates_addon_"):
                                logging.debug("Docplates:      - Skipping %s (Doesn't start with 'docplates_addon_')", zip_item)
                                continue
                            # It seems to match add to the list
                            zip_dirs.append(zip_item)
                        # Loop with the directory canditates we got and look for __init__.py
                        for zip_item in zip_dirs:
                            # If the filename doesn't have an init, just continue
                            if f"{zip_item.filename}__init__.py" not in zip_file.namelist():
                                logging.debug(
                                    "Docplates:    - Skipping directory, does not contain __init__.py: %s", zip_item.filename
                                )
                                continue
                            # Add path to addon dir
                            addon_dir_name = zip_item.filename.split("/")[0]
                            addon_list.update({addon_dir_name: str(addon_path)})
                            logging.debug("Docplates:    - Addon found: %s", addon_dir_name)

                # Check if the addon path exists as a dir
                elif addon_path.is_dir():
                    logging.debug("Docplates:    - Addon path is a directory, trying to load as package")
                    for addon_dir in addon_path.iterdir():
                        # Work out the path by adding the addon_dir to the addon_path
                        addon_dir_path = addon_path.joinpath(addon_dir)
                        # Skip directories we don't want to consider
                        if not (addon_dir_path.is_dir() and addon_dir_path.parts[-1].startswith("docplates_addon_")):
                            logging.debug(
                                "Docplates:    - Skipping directory, does not start with 'docplates_addon_': %s", addon_dir_path
                            )
                            continue
                        # Check that we have a __init__.py in the directory
                        if not addon_dir_path.joinpath("__init__.py").is_file():
                            logging.debug("Docplates:    - Skipping directory, does not contain __init__.py: %s", addon_dir_path)
                            continue
                        addon_name = str(addon_dir.parts[-1])
                        addon_list.update({addon_name: str(addon_path)})
                        logging.debug("Docplates:    - Addon found: %s", addon_name)

                # Else throw an error
                else:
                    raise DocplatesError(f"Add-on path '{addon_path}' does not exist")

            # Save sys paths
            sys_paths = sys.path.copy()

            # Add addon paths to the sys paths
            sys.path = [*set(addon_list.values()), *sys.path]
            # Loop with the addons and try load them
            for addon in addon_list:
                self.plugin_manager.load_package(addon)

            # Restore system paths
            sys.path = sys_paths

    def _create_template_environment(
        self, template_paths: List[pathlib.Path], variables: Dict[str, Any]
    ) -> jinja2.sandbox.SandboxedEnvironment:
        """
        Create template environment.

        Parameters
        ----------
        template_paths : :class:`List` [ :class:`~pathlib.Path` ]
            Template paths to add to the environment search paths list.

        variables : :class:`Dict` [ :class:`str`, :class:`Any` ]
            Variables passed to the template environment as globals.

        Returns
        -------
        :class:`jinja2.sandbox.SandboxedEnvironment` :
            Sandboxed environment.

        """

        # This should never be reached, but we test it to make linting happy
        if not self._template_backend:  # pragma: no cover
            raise DocplatesError("No template backend")

        # Initialize the template loader
        loaders: List[DocplatesLoader] = [
            DocplatesFilesystemLoader(
                search_paths=template_paths,
                template_extensions=self._template_backend.template_extensions,
                resource_extensions=self._template_backend.resource_extensions,
            ),
            DocplatesPluginLoader(
                plugin_manager=self._plugin_manager,
                search_paths=template_paths,
                template_extensions=self._template_backend.template_extensions,
                resource_extensions=self._template_backend.resource_extensions,
            ),
        ]
        template_loader = jinja2.ChoiceLoader(loaders)

        # Render first with jinja
        template_env = jinja2.sandbox.SandboxedEnvironment(
            loader=template_loader,
            extensions=["jinja2.ext.do"],
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=jinja2.StrictUndefined,
            autoescape=False,
            # Add our template backend environment options
            **self._template_backend.jinja_environment_options,
        )

        # Load our globals
        template_env.globals.update(self._template_globals)
        template_env.globals.update(variables)
        # Add our own globals
        template_env.globals["export"] = self._globals_export
        template_env.globals["datetime"] = datetime.datetime
        template_env.globals["timedelta"] = datetime.timedelta
        template_env.globals["use_resource"] = self._globals_use_resource

        # Load the filters we added above
        template_env.filters.update(self._template_filters)

        # Grab templates and resources for debugging below
        templates_found = []
        resources_found = []
        for loader in loaders:
            resources_found.extend(loader.get_all_resources())
            templates_found.extend(loader.get_all_templates())

        logging.debug("Docplates: Templates Available")
        for tmpl in templates_found:
            logging.debug("Docplates:  - %s", tmpl)

        logging.debug("Docplates: Resources Available")
        for rsrc in resources_found:
            logging.debug("Docplates:  - %s", rsrc)

        logging.debug("Docplates: Environment Globals Available")
        for name, value in sorted(template_env.globals.items()):
            logging.debug("Docplates:  - %s = %s", name, str(value))

        logging.debug("Docplates: Environment Filters Available")
        for name, value in sorted(template_env.filters.items()):
            logging.debug("Docplates:  - %s = %s", name, str(value))

        return template_env

    def _globals_export(self, name: str, value: Any) -> None:
        """
        Resolve the resource name and provide it to the backend renderer.

        Parameters
        ----------
        context : :class:`~jinja2.runtime.Context`
            Context passed to us by Jinja2.

        name : :class:`str`
            Variable name.

        value : :class:`Any`
            Variable value.

        """

        logging.debug("Docplates: Got export request for '%s'", name)

        self._exports[name] = value

    @jinja2.pass_context
    def _globals_use_resource(  # pylint: disable=no-self-use
        self, context: jinja2.runtime.Context, resource_name: str, strip_extension: bool = False, render: bool = False
    ) -> str:
        """
        Resolve the resource name and provide it to the backend renderer.

        Parameters
        ----------
        context : :class:`~jinja2.runtime.Context`
            Context passed to us by Jinja2.

        resource_name : :class:`str`
            Resource name to return path of.

        strip_extension : :class:`bool`
            Strip extension of the resource, this is primarily used for Latex and /includegraphics which takes no extension.

        render : :class:`bool`
            Indicate that the resource is a template and should be passed through the template engine to before making it available
            to the backend renderer.

        """

        # This should never be reached, we add it here just incase
        if not getattr(context.environment, "loader"):  # noqa: B009 # pragma: no cover
            raise DocplatesError("Environment has no 'loader' attribute")

        loaders = getattr(context.environment.loader, "loaders")  # noqa: B009
        # This should never be reached, we add it here just incase
        if not loaders:  # pragma: no cover
            raise DocplatesError("Environment loader has no 'loaders' attribute")

        # Loop with loaders, we cannot use Jinja2 as it doesn't support our non-template resources
        # So what we do here is we pull out the list of loaders from ChoiceLoader
        for loader in loaders:
            # This should never be reached, we add it here just incase and to make linting happy
            if not isinstance(loader, DocplatesLoader):  # pragma: no cover
                raise DocplatesError("Loader is not a DocplatesLoader")
            # Try grab resource
            resource = loader.get_resource(environment=context.environment, resource_name=resource_name, render=render)
            # Check if we actually got it
            if resource:
                # Check if we need to strip the extension
                if strip_extension:
                    # If we do, just strip one extension component
                    return str(pathlib.Path(resource.name).with_suffix(""))
                # Return the resource name as is
                return resource.name

        # If we didn't find a resource we need to raise an exception
        raise DocplatesResourceNotFoundError(name=resource_name, message=f"Resource '{resource_name}' not found")

    def _copy_resources(  # pylint: disable=no-self-use
        self, resources: List[DocplatesLoaderResource], destination: pathlib.Path
    ) -> None:
        """
        Copy our resourcs to the destination path.

        Parameters
        ----------
        resources : :class:`List` [ :class:`DocplatesLoaderResource` ]
            Resources to copy.

        destination : :class:`~pathlib.Path`
            Destination path.

        """

        logging.debug("Docplates: Copying resources to: %s", destination)

        # Loop with resources
        for resource in resources:
            logging.debug("Docplates:   - %s (render=%s)", resource.name, resource.render)
            # Join the resource name to the destination path
            destination_path = destination.joinpath(resource.name)

            # Make sure the destination directory exists
            destination_path.parent.mkdir(0o750, parents=True, exist_ok=True)

            # Write out resource
            with destination_path.open("wb") as destination_file:
                destination_file.write(resource.as_binary())

    @property
    def plugin_manager(self) -> ezplugins.EZPluginManager:
        """
        Docplates plugin manager.

        Returns
        -------
        :class:`~ezplugins.EZPluginManager` :
            Docplates plugin manager.

        """
        return self._plugin_manager

    @property
    def exports(self) -> Dict[str, Any]:
        """
        Variables exported from template.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`Any` ] :
            Variables exported from template.

        """
        return self._exports

    @property
    def template_search_paths(self) -> List[pathlib.Path]:
        """
        Template search paths. During document generation the template file path will be added first in the list.

        Returns
        -------
        :class:`List` [ :class:`~pathlib.Path` ] :
            List of template sarch paths.

        """
        return self._template_search_paths
