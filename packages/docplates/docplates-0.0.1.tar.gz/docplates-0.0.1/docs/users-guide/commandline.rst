.. _Command Line Usage:

Command Line Usage
==================



Basic Usage
-----------

The basic command line usage for Docplates would be just to specify a template file to render:

.. code-block:: shell

    docplates mytemplate.tex

Or using HTML templates:

.. code-block:: shell

    docplates mytemplate.html



Configuration File
------------------

By default Docplates uses a default configuration file path of ``~/.config/docplates.conf``. This can be overridden using the
``--config-file`` option.

An example of using this can be found below:

.. code-block:: shell

    docplates --config-file test.conf mytemplate.tex

More information on the contents of the configuration file can be found in :ref:`Configuration`.



PDF Output Options
------------------

By default a template would have a resulting PDF created in a subdirectory which is timestamped, for example
``docplates helloworld.tex`` would result in a PDF ``helloworld - YYYYMMDDHHMM/helloworld - YYYYMMDDHHMM/helloworld.pdf``.

Ouptut PDF files are also encrypted with a random string to ensure compliance with various legislations around the world in terms
of prevention of modification. This is commonly a requirement for invoices.

Despite these defaults the output behavior can be changed with a number of options below.

--output-file
    The resulting PDF output filename can be overridden using the ``--output-file`` option. Using either ``--no-timestamp`` or
    ``--no-subdir`` in addition to this option will result in an error.

--no-encryption
    Do not encrypt the resulting PDF. Pretty straight forward, by default the resulting PDF is encrypted, using this option would
    result in the output PDF not being encrypted.

--no-subdir
    By default the resulting PDF is placed into a timestamped directory. Using this option would prevent the creation of this
    subdirectory and place the resulting PDF alongside the template it was created from.

--no-timestamp
    Resulting PDF files include the timestamp (modification time of the template file passed on the commandline) in their name, this
    makes it somewhat easy to make changes and compare the resulting PDF with previous PDF's. It also makes it easy to determine
    exactly which document is being referred to when this is included in the document or in the document metadata.

    Using the ``DOCUMENT_NAME`` global and the ``hyperref`` LaTeX package, the document name can be included in the PDF metadata.
    For including metadata in HTML when using the WeasyPrint HTML renderer, check out `WeasyPrint Metadata`_.

.. _WeasyPrint Metadata: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html#weasyprint.document.DocumentMetadata



Loading Data Into Templates
---------------------------

Sometimes it may be necessary to load data into a template and generate a PDF using that data. Docplates allows one to do this
with the ``--load-data`` option.

To set a specific global variable from the command line the ``--set`` option can be used.

Both these options are detailed below.

--load-data
    Allows the loading of data using a ``.yaml`` or ``.json`` data file. This data will be available in the ``data`` global.

    The expected format of the data file depends on it's extension. YAML will be expected to be found in a ``.yaml`` file and JSON
    would be expected to be found in a ``.json`` file.

--set NAME=VALUE / --set NAME+=VALUE
    This command line option allows setting of a template global to the specified value, this is a quick and easy way to customize
    template generation from the commandline.

    For example the following could be used:

    .. code-block:: shell

        docplates --set SOMEVAR=SOMEVAL

    You can also specify an array as a resulting data type using the following, it is important to note that if a second value
    is specified with ``+=`` it will transfrom the variable into an array. If both had ``=`` it would of overwritten the first
    value:

    .. code-block:: shell

        docplates --set SOMEVAR=SOMEVAL1 --set SOMEVAR+=SOMEVAL2
        docplates --set SOMEVAR+=SOMEVAL1 --set SOMEVAR+=SOMEVAL2

    One could use this in an ``if`` statment or escape it and include it in the PDF document itself:

    .. code-block::

        \VAR{ SOMEVAR | escape }



Exporting Data From Templates
-----------------------------

Data can also be exported from templates, this may be common where complex calculations are taking place within a specific addon
and the values need to be captured and fed into another software package.

--export [EXPORT]
    If ``--export`` is used without a parameter the default export file will be the output PDF filename with a ``.json`` extension.
    One can export to STDOUT using ``-`` as a paremeter, or specify the filename to export to using anything else. Just to
    re-iterate the default output format is JSON, this can be adjusted below.

--export-format {json,yaml}
    Format of the exported data. This can be specified as JSON using ``json`` or YAML using ``yaml`` as a parameter to this
    argument. The default output format is ``json``.



Debugging & Troubleshooting
---------------------------

There are a number of options that can be used for debugging discussed below.


--preserve-build
    Preserve files used to build the PDF, by default this would be in a ``build/`` sub-directory if you are not using
    ``--no-subdir``. If you are using ``--no-subdir`` then ``.build`` is appending to the resulting filename and this is used
    as a directory to place the preserved files.

    The preserved files are those used by the renderer to render the PDF.


--list-modules
    List all Python modules loaded. This is used more for development, but will show all Python modules loaded by Docplates and
    any addons being utilized.


--list-plugins
    List all Docplates plugins loaded. This includes plugins used internally by Docplates aswell as addons loaded via the plugin
    system.


--list-template-search-paths
    List template search paths. This will exclude the directory where the template file is located on output as this is only added
    during document generation. The template file directory is added first in the list.


--verbose
    The verbose option will print excessive debug information about the inner workings of Docplates during execution. This can
    be used to determine where problems may lie or why plugins or addons are not being loaded.

    For instance this can be combined with ``--list-plugins`` to confirm addons are being loaded correctly by the plugin system.



Exit Codes
----------

    0
        Normal exit.

    2
        Configuration file error.

    3
        Template error.
