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

"""Docplates loaders."""


import importlib.abc
import importlib.resources
import logging
import os
import pathlib
import sys
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import ezplugins
import jinja2
import jinja2.loaders
import jinja2.utils

from .exceptions import DocplatesError, DocplatesResourceNotFoundError

__all__ = [
    "DocplatesLoader",
    "DocplatesLoaderResource",
    "DocplatesFilesystemLoader",
    "DocplatesPluginLoader",
]

DocplatesTemplateSourceType = Tuple[str, Optional[str], Optional[Callable[[], bool]]]
DocplatesTemplateSearchPathsType = Union[str, os.PathLike[Any], Sequence[Union[str, os.PathLike[Any]]]]


class DocplatesLoaderResource:
    """
    Docplates loader resource. When a resource is loaded this object is instantiated to track it.

    Later on before the document is rendered, all resources are copied to the temporary directory where the template is
    rendered.

    Parameters
    ----------
    name : :class:`str`
        Resource name, this is the basic path, eg. something/file.tex or something/images/file.pdf

    resource : :class:`Union` [ :class:`pathlib.Path`, :class:`importlib.abc.Transversable`, :class:`str` ]
        Resource handle. Either a :class:`pathlib.Path`, :class:`importlib.abc.Transversable` or :class:`str`.

    loaded_from : :class:`str`
        This indicates where the resource was loaded from.

    render : :class:`bool`
        This resource requires rendering with the template engine.

    """

    _name: str
    _resource: Union[pathlib.Path, importlib.abc.Traversable, str]
    _render: bool
    _loaded_from: Optional[str]

    def __init__(
        self,
        name: str,
        resource: Union[pathlib.Path, importlib.abc.Traversable, str],
        loaded_from: Optional[str] = None,
        render: bool = False,
    ):
        """
        Docplates loader resource. When a resource is loaded this object is instantiated to track it.

        Later on before the document is rendered, all resources are copied to the temporary directory where the template is
        rendered.

        Parameters
        ----------
        name : :class:`str`
            Resource name, this is the basic path, eg. something/file.tex or something/images/file.pdf

        resource : :class:`Union` [ :class:`pathlib.Path`, :class:`importlib.abc.Transversable`, :class:`str` ]
            Resource handle. Either a :class:`pathlib.Path`, :class:`importlib.abc.Transversable` or :class:`str`.

        loaded_from : :class:`str`
            This indicates where the resource was loaded from.

        render : :class:`bool`
            This resource requires rendering with the template engine.

        """
        self._name = name
        self._resource = resource
        self._loaded_from = loaded_from
        self._render = render

    def as_binary(self) -> bytes:
        """
        Return contents of the resource in binary.

        Returns
        -------
        :class:`bytes` :
            Contents of resource in binary.

        """

        # Grab file contents
        if isinstance(self._resource, str):
            return self._resource.encode("UTF-8")
        if isinstance(self._resource, pathlib.Path):
            with self._resource.open("rb") as template_file:
                return template_file.read()
        elif isinstance(self._resource, importlib.abc.Traversable):
            return self._resource.read_bytes()

        # NK: This cannot easily be reached unless an invalid resource was somehow loaded
        raise DocplatesError(f"Invalid resource '{self.name}'")  # pragma: no cover

    def as_text(self, encoding: str = "UTF-8") -> str:
        """
        Return contents of the resource as text.

        Returns
        -------
        :class:`str` :
            Contents of resource in a string.

        """
        # Grab file contents
        # NK: We don't use string resources at present
        if isinstance(self._resource, str):  # pragma: no cover
            return self._resource
        if isinstance(self._resource, pathlib.Path):
            with self._resource.open("r", encoding=encoding) as template_file:
                return template_file.read()
        # NK: I've not managed to find a way to reach this bit of code yet
        elif isinstance(self._resource, importlib.abc.Traversable):  # pragma: no cover
            return self._resource.read_text(encoding="UTF-8")

        # NK: Reaching this code would require an invalid resource to of somehow been loaded
        raise DocplatesError(f"Invalid resource '{self.name}'")  # pragma: no cover

    def __str__(self) -> str:
        """
        Return a string representation of this object.

        Returns
        -------
        :class:`str` :
            String representation of the object.

        """

        return f"{self.name} from {self.loaded_from}"

    @property
    def name(self) -> str:
        """
        Resource name, template path in this case.

        Returns
        -------
        :class:`str` :
            Return the resource name.

        """

        return self._name

    @property
    def path(self) -> str:
        """
        Resource path.

        Returns
        -------
        :class:`str` :
            Return the resource path.

        """
        # We just return [string] for a string resource
        # NK: We don't use string resources yet
        if isinstance(self._resource, str):  # pragma: no cover
            return "[string]"
        return str(self._resource)

    @property
    def loaded_from(self) -> Optional[str]:
        """
        Text description of where the resource was loaded from.

        Returns
        -------
        :class:`Optional` [ :class:`str` ]:
            Return where the resource was loaded from.

        """

        return self._loaded_from

    @property
    def render(self) -> bool:
        """
        Resource must be rendered.

        Returns
        -------
        :class:`bool` :
            Return if the resource should be rendered or not.

        """

        return self._render


class DocplatesLoader(jinja2.BaseLoader):
    """
    Docplates loader base class.

    This is our base class which tracks templates and resources used during parsing the template.

    Parameters
    ----------
    template_extensions : :class:`List` [ :class:`str` ]
        List of template file extensions. Files without these extensions will not be considered as templates.

    resource_extensions : :class:`List` [ :class:`str` ]
        List of resource file extensions. Files without these extensions will not be considered as resources.

    encoding : :class:`str`
        Use this encoding to read the text from template files.

    """

    _template_extensions: List[str]
    _resource_extensions: List[str]
    _encoding: str

    _loaded_templates: Dict[str, DocplatesLoaderResource]
    _loaded_resources: Dict[str, DocplatesLoaderResource]

    def __init__(
        self,
        template_extensions: List[str],
        resource_extensions: List[str],
        encoding: str = "UTF-8",
    ) -> None:
        """
        Docplates loader base class.

        This is our base class which tracks templates and resources used during parsing the template.

        Parameters
        ----------
        template_extensions : :class:`List` [ :class:`str` ]
            List of template file extensions. Files without these extensions will not be considered as templates.

        resource_extensions : :class:`List` [ :class:`str` ]
            List of resource file extensions. Files without these extensions will not be considered as resources.

        encoding : :class:`str`
            Use this encoding to read the text from template files.

        """

        self._template_extensions = template_extensions
        self._resource_extensions = resource_extensions
        self._encoding = encoding

        self._loaded_templates = {}
        self._loaded_resources = {}

    def get_source(self, environment: jinja2.Environment, template: str) -> DocplatesTemplateSourceType:
        """
        Get template source.

        Parameters
        ----------
        environment : :class:`jinja2.Environment`
            Jinja2 environment.

        template : :class:`str`
            Template name to load.

        Returns
        -------
        :class:`DocplatesTemplateSourceType` :
            A Tuple containing the contents of the file, the filename, and a callable which returns a bool indicating if the file
            has changed.

        """

        logging.debug("Docplates Loader: Looking for template: %s", template)

        resource = self._get_resources(self._template_extensions, template)
        if not resource:
            raise jinja2.TemplateNotFound(template)

        # Grab found resource, its the first one in the list
        found_resource = resource[0]

        # Add template filename to the loaded templates list
        self.loaded_templates[template] = found_resource

        logging.debug("Docplates Loader: Found template: %s", template)

        return found_resource.as_text(), template, None

    def get_resource(
        self, environment: jinja2.Environment, resource_name: str, render: bool = False
    ) -> Optional[DocplatesLoaderResource]:
        """
        Get a resource.

        Parameters
        ----------
        environment : :class:`jinja2.Environment`
            Jinja2 environment.

        resource_name : :class:`str`
            Resource name to load.

        render : :class:`bool`
            Indicate that the resource needs to be rendered with the template engine.

        Returns
        -------
        :class:`Optional` [ :class:`DocplatesLoaderResource` ] :
            Docplates loader resource if found, if not found we just return :class:`None`.

        """

        logging.debug("Docplates Loader: Looking for resource: %s (render: %s)", resource_name, render)
        # Check if the resource is already added
        # NK: This is cached by Jinja2? so we don't reach this code even with double includes
        if resource_name in self.loaded_resources:  # pragma: no cover
            resource = self.loaded_resources[resource_name]
            logging.debug("Docplates Loader: Resource already loaded: %s", resource)
            return resource

        # Try grab resource
        resources = self._get_resources(extensions=self._resource_extensions, resource_name=resource_name, render=render)
        if not resources:
            return None

        # Grab found resource, its the first one in the list
        resource = resources[0]

        if render:
            # This comes from the "from_string" function in jinja2.Environment (environment.py)
            # NK: We do this so we can override the resource name and disk path
            # NK: We use a blank global list here
            environment_globals = environment.make_globals({})
            template = environment.template_class.from_code(
                environment, environment.compile(resource.as_text(), resource_name, resource.path), environment_globals, None
            )
            # Re-package the rendered output
            self.loaded_resources[resource_name] = DocplatesLoaderResource(
                resource_name, template.render(), loaded_from=f"{resource.loaded_from} [RENDERED]", render=render
            )
        else:
            # Add template filename to the loaded resources list
            self.loaded_resources[resource_name] = resource

        logging.debug("Docplates Loader: Found resource: %s (render=%s)", resource.name, render)

        return resource

    # NK: No real reason to test this, it just returns a list
    def list_resources(self) -> List[str]:  # pragma: no cover
        """
        Return a list of the resources found.

        Returns
        -------
        :class:`List` [ :class:`str` ] :
            List of resources found.

        """
        return [x.name for x in self.get_all_resources()]

    # NK: No real reason to test this, it just returns a list
    def list_templates(self) -> List[str]:  # pragma: no cover
        """
        Return a list of the templates found.

        Returns
        -------
        :class:`List` [ :class:`str` ] :
            List of templates found.

        """
        return [x.name for x in self.get_all_templates()]

    def get_all_resources(self) -> List[DocplatesLoaderResource]:
        """
        Return all resources found.

        Returns
        -------
        :class:`List` [ :class:`DocplatesLoaderResource` ] :
            All resources found.

        """
        return self._get_resources(extensions=self._resource_extensions)

    def get_all_templates(self) -> List[DocplatesLoaderResource]:
        """
        Return all templates found.

        Returns
        -------
        :class:`List` [ :class:`DocplatesLoaderResource` ] :
            All templates found.

        """
        return self._get_resources(extensions=self._template_extensions)

    def _get_resources(  # pylint: disable=unused-argument,no-self-use
        self, extensions: List[str], resource_name: Optional[str] = None, render: bool = False
    ) -> List[DocplatesLoaderResource]:
        """
        Find resource in our plugins.

        Parameters
        ----------
        extensions : :class:`List` [ :class:`str` ]
            List of resource filename extensions to look for.

        resource_name : :class:`str`
            Optional resource name to find. If specified, the resulting list will only contain this item if found.

        Returns
        -------
        :class:`List` [ :class:`DocplatesLoaderResource` ]
            List of resources found.

        """

        # Intercept before we look, so we can raise an exception if the extension is unsupported
        if resource_name and resource_name.split(".")[-1] not in extensions:
            raise DocplatesResourceNotFoundError(
                resource_name, f"Resource '{resource_name}' has unsupported extension, use: {', '.join(extensions)}"
            )

        return []

    @property
    def loaded_templates(self) -> Dict[str, DocplatesLoaderResource]:
        """
        Map of template name to resource.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`DocplatesLoaderResource` ]
            Return the mapping of template names to :class:`DocplatesLoaderResource`.

        """

        return self._loaded_templates

    @property
    def loaded_resources(self) -> Dict[str, DocplatesLoaderResource]:
        """
        Map of resource name to resource.

        Returns
        -------
        :class:`Dict` [ :class:`str`, :class:`DocplatesLoaderResource` ]
            Return the mapping of resource names to :class:`DocplatesLoaderResource`.

        """

        return self._loaded_resources


class DocplatesFilesystemLoader(DocplatesLoader):
    """
    Load templates from a directory in the file system.

    The path can be relative or absolute. Relative paths are relative to
    the current working directory::

        loader = DocplatesFileSystemLoader("templates", template_extensions=["tmpl"])

    A list of paths can be given. The directories will be searched in
    order, stopping at the first matching template::

        loader = FileSystemLoader(["/override/templates", "/default/templates"], template_extensions=["tmpl"])

    Parameters
    ----------
    search_paths : :class:`DocplatesTemplateSearchPathsType`
        A path, or list of paths, to the directory that contains the templates.

    template_extensions : :class:`List` [ :class:`str` ]
        List of template file extensions. Files without these extensions will not be considered as templates.

    resource_extensions : :class:`List` [ :class:`str` ]
        List of resource file extensions. Files without these extensions will not be considered as resources.

    encoding : :class:`str`
        Use this encoding to read the text from template files.

    """

    _search_paths: List[str]

    def __init__(
        self,
        search_paths: DocplatesTemplateSearchPathsType,
        template_extensions: List[str],
        resource_extensions: List[str],
        encoding: str = "UTF-8",
    ) -> None:
        """
        Load templates from a directory in the file system.

        The path can be relative or absolute. Relative paths are relative to
        the current working directory::

            loader = DocplatesFileSystemLoader("templates", template_extensions=["tmpl"])

        A list of paths can be given. The directories will be searched in
        order, stopping at the first matching template::

            loader = FileSystemLoader(["/override/templates", "/default/templates"], template_extensions=["tmpl"])

        Parameters
        ----------
        search_paths : :class:`DocplatesTemplateSearchPathsType`
            A path, or list of paths, to the directory that contains the templates.

        template_extensions : :class:`List` [ :class:`str` ]
            List of template file extensions. Files without these extensions will not be considered as templates.

        resource_extensions : :class:`List` [ :class:`str` ]
            List of resource file extensions. Files without these extensions will not be considered as resources.

        encoding : :class:`str`
            Use this encoding to read the text from template files.

        """

        super().__init__(template_extensions=template_extensions, resource_extensions=resource_extensions, encoding=encoding)

        # NK: We don't currently use other search paths, not sure how this could be reachable?
        if not isinstance(search_paths, Iterable) or isinstance(search_paths, str):  # pragma: no cover
            search_paths = [search_paths]

        self._search_paths = [os.fspath(p) for p in search_paths]

    def _get_resources(  # pylint: disable=too-many-locals
        self, extensions: List[str], resource_name: Optional[str] = None, render: bool = False
    ) -> List[DocplatesLoaderResource]:
        """
        Find resource in our plugins.

        Parameters
        ----------
        extensions : :class:`List` [ :class:`str` ]
            List of resource filename extensions to look for.

        resource_name : :class:`str`
            Optional resource name to find. If specified, the resulting list will only contain this item if found.

        render : :class:`bool`
            Indicate if the resource should be rendered.

        Returns
        -------
        :class:`List` [ :class:`~DocplatesLoaderResource` ]
            List of resources found.

        """

        # Do some checks in our super class
        super()._get_resources(extensions=extensions, resource_name=resource_name, render=render)

        resource_list: List[DocplatesLoaderResource] = []

        # Loop with search paths
        for search_path_str in self._search_paths:
            search_path = pathlib.Path(search_path_str)
            search_path_part_len = len(search_path.parts)
            # Grab all dirs
            walk_dir = os.walk(search_path, followlinks=False)

            # Get the directory and filenames in it
            for dirpath, _, filenames in walk_dir:
                relative_path = pathlib.Path().joinpath(*pathlib.Path(dirpath).parts[search_path_part_len:])

                # Loop with each filename
                for filename in filenames:
                    # Make sure the extension matches the supported extensions
                    if filename.split(".")[-1] not in extensions:
                        continue
                    # Generate the template name
                    fs_resource = pathlib.Path().joinpath(dirpath, filename)
                    fs_resource_name = str(pathlib.Path().joinpath(relative_path, filename))
                    # If we have a name specified, check for a match
                    if not resource_name:
                        # If not, add to the list
                        resource_list.append(
                            DocplatesLoaderResource(
                                name=fs_resource_name,
                                resource=fs_resource,
                                loaded_from=f"{self.__class__.__name__}({fs_resource})",
                                render=render,
                            )
                        )
                    elif resource_name == fs_resource_name:
                        # If it matches, return just this result
                        logging.debug("Docplates Filesystem Loader:   - Returned filesystem resource: %s", resource_name)
                        return [
                            DocplatesLoaderResource(
                                name=fs_resource_name,
                                resource=fs_resource,
                                loaded_from=f"{self.__class__.__name__}({fs_resource})",
                                render=render,
                            )
                        ]

        # Return the sorted list of templates found
        return resource_list


class DocplatesPluginLoader(DocplatesLoader):
    """
    Load templates from a plugin.

    The paths are relative to the plugin package::

        loader = DocplatesFileSystemLoader(plugin_manager, "templates", extensions=["tmpl"])

    A list of paths can be given. The plugin data resources will be searched in
    order, stopping at the first matching template::

        loader = FileSystemLoader(plugin_manager, ["/override/templates", "/default/templates"], extensions=["tmpl"])

    Parameters
    ----------
    plugin_manager : :class:`ezplugins.EZPluginManager`
        EZ plugin manager.

    search_paths : class:`DocplatesTemplateSearchPathsType`
        A path, or list of paths, to the directory that contains the templates.

    template_extensions : :class:`List` [ :class:`str` ]
        List of template file extensions. Files without these extensions will not be considered as templates.

    resource_extensions : :class:`List` [ :class:`str` ]
        List of resource file extensions. Files without these extensions will not be considered as resources.

    encoding : :class:`str`
        Use this encoding to read the text from template files.

    """

    _plugin_manager: ezplugins.EZPluginManager
    _search_paths: List[str]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        plugin_manager: ezplugins.EZPluginManager,
        search_paths: DocplatesTemplateSearchPathsType,
        template_extensions: List[str],
        resource_extensions: List[str],
        encoding: str = "UTF-8",
    ) -> None:
        """
        Load templates from a plugin.

        The paths are relative to the plugin package::

            loader = DocplatesFileSystemLoader(plugin_manager, "templates", template_extensions=["tmpl"])

        A list of paths can be given. The plugin data resources will be searched in
        order, stopping at the first matching template::

            loader = FileSystemLoader(plugin_manager, ["/override/templates", "/default/templates"], template_extensions=["tmpl"])

        Parameters
        ----------
        plugin_manager : :class:`ezplugins.EZPluginManager`
            EZ plugin manager.

        search_paths : :class:`DocplatesTemplateSearchPathsType`
            A path, or list of paths, to the directory that contains the templates.

        template_extensions : :class:`List` [ :class:`str` ]
            List of template file extensions. Files without these extensions will not be considered as templates.

        resource_extensions : :class:`List` [ :class:`str` ]
            List of resource file extensions. Files without these extensions will not be considered as resources.

        encoding : :class:`str`
            Use this encoding to read the text from template files.

        """

        super().__init__(template_extensions=template_extensions, resource_extensions=resource_extensions, encoding=encoding)

        # NK: We don't currently use other search paths, not sure how this could be reachable?
        if not isinstance(search_paths, Iterable) or isinstance(search_paths, str):  # pragma: no cover
            search_paths = [search_paths]

        # Grab plugin manager and search paths
        self._plugin_manager = plugin_manager
        self._search_paths = [os.fspath(p) for p in search_paths]

    def get_source(self, environment: jinja2.Environment, template: str) -> DocplatesTemplateSourceType:
        """
        Get template source.

        Parameters
        ----------
        environment : :class:`jinja2.Environment`
            Jinja2 environment.

        template : :class:`str`
            Template name to load.

        Returns
        -------
        class:`DocplatesTemplateSourceType` :
            A Tuple containing the contents of the file, the filename, and a callable which returns a bool indicating if the file
            has changed.

        """

        template_parts = list(pathlib.Path(template).parts)
        # We only intercept lib/ here...
        if template_parts[0] != "lib":
            raise jinja2.TemplateNotFound(template)

        template_new = pathlib.Path(*template_parts)

        return super().get_source(environment, str(template_new))

    def _get_resources(
        self, extensions: List[str], resource_name: Optional[str] = None, render: bool = False
    ) -> List[DocplatesLoaderResource]:
        """
        Find resource in our plugins.

        Parameters
        ----------
        extensions : :class:`List` [ :class:`str` ]
            List of resource filename extensions to look for.

        resource_name : :class:`str`
            Optional resource name to find. If specified, the resulting list will only contain this item if found.

        render : :class:`bool`
            Indicate if the resource should be rendered.

        Returns
        -------
        :class:`List` [ :class:`~DocplatesLoaderResource` ]
            List of resources found.

        """

        # Do some checks in our super class
        super()._get_resources(extensions=extensions, resource_name=resource_name, render=render)

        # List of templates found
        resource_list: List[DocplatesLoaderResource] = []

        # Loop with loaded plugins
        for ezmodule in self._plugin_manager.modules:
            # Grab the module
            module = ezmodule.module
            # See if its part of a package, if not just continue
            # NK: Probably not reachable under any easy circumstances?
            if not module.__package__:  # pragma: no cover
                continue
            # Grab the module package
            package = sys.modules[module.__package__]

            # Make sure we have a templates resource
            if "templates" not in importlib.resources.contents(package):
                continue

            # Work out the base directory path for this module
            base_dir_path = pathlib.Path(str(package.__path__))

            # Work out path of template relative to the base directory path of the module
            base_dir_path_len_with_templates = len(base_dir_path.parts) + 1  # Make linting happy below with : having a space after

            # Start with the top level template directory in the list of directories to process
            search_dirs = [importlib.resources.files(package).joinpath("templates")]
            # Loop while we have template_dirs
            while search_dirs:
                # Grab next item
                search_dir = search_dirs.pop(0)
                # Make sure the templates folder is a dir and not a file
                # NK: Reachable if the templates/ directory is actually a file
                if not search_dir.is_dir():  # pragma: no cover
                    logging.debug("Docplates Plugin Loader: Template directory '%s' is not a directory", search_dir)
                    continue

                # Grab items in this template directory
                for plugin_item in search_dir.iterdir():
                    # Check if we are a dir, if we are, add to search list and skip to next
                    if plugin_item.is_dir():
                        search_dirs.append(plugin_item)
                        continue
                    # Just continue if this is not a file
                    # NK: Probably only reachable if something is wonky regarding the plugin_item, perhaps a symlink or device file?
                    if not plugin_item.is_file():  # pragma: no cover
                        continue
                    # Skip anything that looks invalid
                    if not [
                        True
                        for x in extensions
                        # Skip things starting with . and anything not ending with our extension
                        if not plugin_item.name.startswith(".") and plugin_item.name.endswith(f".{x}")
                    ]:
                        logging.debug(
                            "Docplates Plugin Loader:   - Resource '%s' does not match %s, skipping", plugin_item.name, extensions
                        )
                        continue

                    # Work out the plugin resource path, relevant to the templates search path
                    plugin_resource_path = pathlib.Path().joinpath(
                        *pathlib.Path(str(plugin_item)).parts[base_dir_path_len_with_templates:]
                    )
                    # Prefix the plugin loader resources with lib/
                    plugin_resource_name = str(pathlib.Path().joinpath("lib", *plugin_resource_path.parts))

                    # If we have a name specified, check for a match
                    if not resource_name:
                        # If not, add to the list
                        resource_list.append(
                            DocplatesLoaderResource(
                                name=plugin_resource_name,
                                resource=plugin_item,
                                loaded_from=f"{self.__class__.__name__}({plugin_resource_path}, {search_dir})",
                                render=render,
                            )
                        )
                    elif resource_name == plugin_resource_name:
                        # If it matches, return just this result
                        logging.debug("Docplates Plugin Loader:   - Returned plugin resource: %s", resource_name)
                        return [
                            DocplatesLoaderResource(
                                name=plugin_resource_name,
                                resource=plugin_item,
                                loaded_from=f"{self.__class__.__name__}({plugin_resource_path}, {search_dir})",
                                render=render,
                            )
                        ]

        # Return the list of resources
        return resource_list
