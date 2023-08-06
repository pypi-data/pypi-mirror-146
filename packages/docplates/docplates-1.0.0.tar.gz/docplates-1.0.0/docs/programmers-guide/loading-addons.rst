Loading Addons
==============

Internally Docplates will load all EZPlugins starting with the name ``docplates_addon_`` installed on the system or found within
the ``addon_paths`` configuration. This includes addons located in Zip files starting with the same name.

Addons can also be loaded manually, in order to load an an addon one needs to create an instance of the
:class:`ezplugins.EZPluginManager` and pass it to Docplates after loading the desired EZPlugins which implement addons.

.. code-block:: python

    import docplates
    import ezplugins

    # Here is where we create an instance for the plugin manager
    plugin_manager = ezplugins.EZPluginManager()
    # And load our plugin here...
    plugin_manager.load_module("some.plugin.name")

    # Create docplates object
    config = {
        "template_search_paths": [
            "~/Docplates/mytemplates1",
            "~/Docplates/mytemplates2",
        ]
    }
    docp = docplates.Docplates(config=config)

    # Load template and get exports
    exports = docp.generate(
        input_file=pathlib.Path("/home/user/tmp/file.tex"),
        output_file=pathlib.Path("/home/user/tmp/file.pdf"),
        variables={"var1": "value1", "var2": "value2"},
    )
