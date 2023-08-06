Quickstart
==========

Package Modules
---------------

Generally when using Docplates, the easiest to import everything one could need is to use the following::

   import docplates

Everything is exported by the package.


Using Docplates
---------------

Probably the most recommended way of integrating Docplates into software is by using the :class:`docplates.Docplates` class.

The :class:`docplates.Docplates` class is used by creating an instance with any desired configuration:

.. code-block:: python

    import docplates

    # Create docplates object
    config = {
        "template_search_paths": [
            "~/Docplates/mytemplates1",
            "~/Docplates/mytemplates2",
        ]
        "addon_paths": [
            "~/Docplates/addons/some_addon",
        ]
    }
    docp = docplates.Docplates(config=config)


Supported configuration options can be found in the class documentation :class:`docplates.Docplates`.

Once the object is instantiated a PDF can be generated using the below example (following on from the above):

.. code-block:: python

    # Load template and get exports
    exports = docp.generate(
        input_file=pathlib.Path("/home/user/tmp/file.tex"),
        output_file=pathlib.Path("/home/user/tmp/file.pdf"),
        variables={"var1": "value1", "var2": "value2"},
    )

The ``exports`` variable will contain any data that was exported by the template, if you're not using it or do not require it then
just leave it out.

For additonal options check out the class documentation for :class:`docplates.Docplates`.



Using DocplatesCommandLine
--------------------------

A great feature of Docplates is you can use it in your software as if it was being executed from the command line.

.. code-block:: python

    import docplates

    docp_cmdline = docplates.DocplatesCommandLine()
    docp_cmdline.run(["--verbose", "/home/user/tmp/file.tex"], setup_console_logging=True)


For addtional options check out the class documentation for :class:`docplates.DocplatesCommandLine`.
