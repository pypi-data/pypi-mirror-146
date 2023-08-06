Quickstart
==========



Introduction
------------

Docplates is based on the Jinja2_ templating engine and will render Jinja2 templates. Check out :ref:`Templates` for more
information.

.. _Jinja2: https://jinja.palletsprojects.com/en/latest/templates/



Your First LaTeX Template
-------------------------

An example is included of a very simple LaTeX file, which has no Jinja2 syntax, in ``examples/helloworld.tex``:

.. code-block:: tex

    \documentclass[12pt]{article}
    \begin{document}
    Hello world!
    \end{document}

This is the most basic form of a template, even though technically it's not a template as it has no template syntax. It can still
be passed to Docplates and a PDF generated.



Running Docplates
-----------------

Docplates can be run from the command line using the ``docplates`` command:

.. code-block:: shell

    docplates examples/helloworld.tex

Where ``examples/helloworld.tex`` is our LaTeX template.

The output from the above would look similar to this::

    Docplates v0.0.1 - Copyright © 2015-2022, AllWorldIT.

    2022-04-06 11:09:19,748 INFO     LaTeX Backend: Generating PDF...
    2022-04-06 11:09:19,929 INFO     LaTeX Backend: Generated 1 page(s)
    2022-04-06 11:09:19,936 INFO     Docplates: Wrote PDF to '/home/user/docplates/examples/helloworld - 202204061053/helloworld - 202204061053.pdf' (ENCRYPTED)

You will notice that the resulting PDF is timestamped and placed into a sub-directory.

Timestamps can be disabled by using ``--no-timestamp`` and placing the PDF in a sub-directory can be disabled using ``--no-subdir``.
Furthermore if you don't want the resulting PDF encrypted, this can be disabled using ``--no-encryption``. All these options are
explained in the ``--help`` output and in :ref:`Command Line Usage`.

The resulting PDF should look something like this:

.. image:: images/helloworld.png
    :width: 200
    :alt: Image of the helloworld.tex PDF



Configuration
-------------

Docplates supports using a configuration file which can be used to specify template search paths and addon paths, this would
generally be done using the ``~/.config/docplates.conf`` configuration file or by specifying the configuration file on the
commandline using ``--config-file``.

An example of a typical configuration file is below:

.. code-block:: yaml

    template_search_paths:
        - ~/Docplates/mytemplates
        - ~/Docplates/moretemplates

    addon_paths:
        - ~/Docplates/addons/somecooladdon
        - ~/Docplates/addons/anotheraddon

Template directories are searched in order of being configured. Each template search path is expected to have a ``templates/``
folder, if one is not specified it will be added automatically.

Both addon paths are supported along with addon Zip files.

All addons typically start with ``docplates_addon_`` and would be found within the ``addon_path``.



Further Usage
-------------

As Jinja2 is used for the templating engine the use of Docplates is limited only by your imagination and creativity.

One can create a complex system of templates including document layouts, branding and boilerplates for various types of documents.

