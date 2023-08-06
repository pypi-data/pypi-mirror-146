.. _Configuration:

Configuration
=============

Docplates uses the default configuration file path of ``~/.config/docplates.conf``, a configuration file can also be specified on
the commandline using the ``--config-file`` argument.



Configuration Options
---------------------

Configuration options supported include the following:

template_search_paths
    Search paths for templates, this is in the form of a list. The path will have ``templates/`` appended if the path
    does not contain ``templates/`` at the end.

addon_paths
    Addon paths to load into the Docplates, this is in the form of a list. Addon paths can either be directories or Zip files,
    in the case of Zip files all addons matching ``docplates_addon_`` will be loaded from the Zip file.


Both of these are lists and specified in YAML format like in the below example::

    template_search_paths:
        - ~/Docplates/mytemplates
        - ~/Docplates/moretemplates

    addon_paths:
        - ~/Docplates/addons/somecooladdon
        - ~/Docplates/addons/anotheraddon
