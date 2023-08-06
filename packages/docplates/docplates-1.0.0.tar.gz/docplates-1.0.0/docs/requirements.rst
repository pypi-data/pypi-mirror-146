Requirements
============

Docplates requires a few Python packages in order to work, these are explained below. Check out :ref:`Installing & Running` for
various ways to install and run Docplates.


ezplugins
    Mandatory, used for the plugin system.

jinja2
    Mandatory, used for templating.

pikepdf
    Mandatory, use for PDF encryption.

pydyf
    Optional, used when templating ``.html`` files. The HTML templating engine will fail to register without it.

PyYAML
    Mandatory, core feature for exporting of data.

weasyprint
    Optional, used when templating ``.html`` files. The HTML templating engine will fail to register without it.

pango
    Optional, required for WeasyPrint.

texlive
    Required for LaTeX support. Make sure ``/usr/bin/latexmk`` is available.
