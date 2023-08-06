Writing Addons
==============

Docplates addons are based on the EZPlugins plugin library. Information on EZPlugins can be found here `EZPlugins Documentation`_.

.. _EZPlugins Documentation: https://software.pages.oscdev.io/ezplugins/



Writing a Simple Addon
----------------------

Below is a simple addon that adds a global:

.. code-block:: python

    from typing import Any, Callable, Dict, List

    import ezplugins

    import docplates

    __all__: List[str] = []


    @ezplugins.ezplugin
    class Plugin1:  # pylint: disable=too-few-public-methods
        """Docplates test addon."""

        def __init__(self) -> None:
            """Initialize object."""

        @ezplugins.ezplugin_method()  # type: ignore
        def docplates_get_globals(  # pylint: disable=unused-argument,no-self-use
            self, backend: docplates.DocplatesBackend
        ) -> Dict[str, Callable[..., Any]]:
            """
            Returns our test global.

            This global is just used for testing.

            Parameters
            ----------
            backend : :class:`DocplatesBackend`
                Backend that is currently being used.

            Returns
            -------
            :class:`Dict` [ :class:`str`, :class:`Callable` [ ..., :class:`Any` ] ] :
                Dict of globals to return indexed by the global name.

            """

            template_globals = {"test_addon_function": lambda msg: f"Message: {msg}"}

            return template_globals


It does not matter where in the package the EZPlugins are located, EZPlugins will walk through the entire package. As long as the
directory specified as an addon-path contains a directory or directories beginning with ``docplates_addon_``.



Plugin Methods
--------------

docplates_init(plugin_manager: :class:`ezplugins.EZPluginManager`) -> :class:`None`

    The :meth:`docplates_init` method is called with the current plugin manager when an instance of :class:`docplates.Docplates`
    class is created.

    The purpose of this method is to initialize any plugin data that will live between document genreation calls.

    .. code-block:: python

        @ezplugins.ezplugin
        class MyPlugin:  # pylint: disable=too-few-public-methods
            """My plugin."""

            some_data: str


            def __init__(self) -> None:
                """Initialize object."""

                self.some_data = ""

            @ezplugins.ezplugin_method()  # type: ignore
            def docplates_init(self, plugin_manager: ezplugins.EZPluginManager) -> None:  # pylint: disable=no-self-use,unused-argument
                """Initialize docplates addon."""

                self.some_data = "Initailized"


docplates_get_backend(self, template_file: :class:`str``) -> :class:`Optional` [ :class:`docplates.DocplatesBackend` ]

    The :meth:`docplates_get_backend` method is responsible for returning a backend instance if the template filename matches
    the file extension that the backend supports.

    An example of the code that implements the LaTeX backend can be found below:

    .. code-block:: python

        @ezplugins.ezplugin
        class MyBackendPlugin:  # pylint: disable=too-few-public-methods
            """My backend plugin."""

            def __init__(self) -> None:
                """Initialize object."""

            @ezplugins.ezplugin_method()  # type: ignore
            def docplates_get_backend(self, template_file: str) -> Optional[DocplatesBackend]:  # pylint: disable=no-self-use
                """
                Return the backend if we can handle the filename provided.

                Returns
                -------
                :class:`Optional` [ :class:`DocplatesBackend` ] :
                    A DocplatesBackend if it supports the template_file filename.

                """

                if template_file.endswith(".tex"):
                    return DocplatesLatexBackend()

                return None


docplates_get_globals(self, backend: :class:`docplates.DocplatesBackend`) -> :class:`Dict` [ :class:`str` , :class:`Callable` [ ... , :class:`Any` ]]

    An example of the code that implements a simple ``test_addon_function`` global that returns ``Message: {msg}`` can be found
    below:

    .. code-block:: python

        @ezplugins.ezplugin
        class MyGlobalPlugin:  # pylint: disable=too-few-public-methods
            """My global plugin."""

            def __init__(self) -> None:
                """Initialize object."""

            @ezplugins.ezplugin_method()  # type: ignore
            def docplates_get_globals(  # pylint: disable=unused-argument,no-self-use
                self, backend: docplates.DocplatesBackend
            ) -> Dict[str, Callable[..., Any]]:
                """
                Return our test global.

                This global is just used for testing.

                Parameters
                ----------
                backend : :class:`DocplatesBackend`
                    Backend that is currently being used.

                Returns
                -------
                :class:`Dict` [ :class:`str`, :class:`Callable` [ ..., :class:`Any` ] ] :
                    Dict of globals to return indexed by the global name.

                """

                template_globals = {"test_addon_function": lambda msg: f"Message: {msg}"}

                return template_globals


docplates_get_filters(self, backend: :class:`docplates.DocplatesBackend`) -> :class:`Dict` [ :class:`str` , :class:`Callable` [ ... , :class:`Any` ]]

    An example of the code that implements a simple ``my_test_filter`` filter that returns ``{some_text} is a test`` can be found
    below:

    .. code-block:: python

        @ezplugins.ezplugin
        class MyFilterPlugin:  # pylint: disable=too-few-public-methods
            """My filter plugin."""

            def __init__(self) -> None:
                """Initialize object."""

            @ezplugins.ezplugin_method()  # type: ignore
            def docplates_get_filters(  # pylint: disable=unused-argument,no-self-use
                self, backend: DocplatesBackend
            ) -> Dict[str, Callable[..., str]]:
                """
                Return my_test_filter filter.

                This filter just adds "is a test" to the end of a given string.

                Parameters
                ----------
                backend : :class:`DocplatesBackend`
                    Backend that is currently being used.

                Returns
                -------
                :class:`Dict` [ :class:`str` , :class:`Callable` [ ..., :class:`str` ] ] :
                    Dict of filter callables indexed by the filter name.

                """

                filters = {
                    "my_test_filter": lambda some_text: f"{some_text} is a test",
                }

                return filters



Including Templates In Addons
-----------------------------

Templates can be included in addons by placing them in a ``templates/`` folder. These can then be used in document templates by
changing the ``templates/`` to ``lib/``.

A typical layout may look like this::

    docplates_addon_test_mod/__init__.py
    docplates_addon_test_mod/templates/__init__ .py
    docplates_addon_test_mod/templates/cool-template.tex
    docplates_addon_test_mod/templates/subdir2/__init__ .py
    docplates_addon_test_mod/templates/subdir2/even-better-template.tex

Take careful note that the ``__init__.py`` files must be present throughout the hierarchy in order to allow Python to load the
templates as resources from the module.


Addons in Zip Files
-------------------

Together with supporting addons in directories Docplates also supports addons in Zip files.

An addon Zip file is created by zipping up the addon module, an example of its contents would be as follows::

    docplates_addon_test_mod/__init__.py
    docplates_addon_test_mod/templates/__init__ .py
    docplates_addon_test_mod/templates/cool-template.tex
    docplates_addon_test_mod/templates/subdir2/__init__ .py
    docplates_addon_test_mod/templates/subdir2/even-better-template.tex

Zipped up using the following command:

.. code-block: shell

    zip -r ../myaddon.zip docplates_addon_test_mod

This would be loaded using the following configuration:

    addon_paths = ["/home/user/Docplates/addons/myaddon.zip"]

As easy as that!
