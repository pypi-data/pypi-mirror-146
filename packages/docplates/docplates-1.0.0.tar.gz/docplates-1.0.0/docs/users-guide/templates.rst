.. _Templates:

Templates
==========

Docplates supports both ``.tex`` templates using LaTeX and ``.html`` templates using WeasyPrint.

Jinja2_ is used for templating, with a slightly customized environment for LaTeX. HTML remains with the defeault tag names.

.. _Jinja2: https://jinja.palletsprojects.com/en/latest/templates/

It is important to note that any assets needed for these two templates be included using the `use_resource`_ built-in below.

The current working directory where Docplates is executed is added in the search path.



Jinja2 Syntax For Latex
-----------------------

Docplates uses a somewhat modified syntax with LaTeX for a more understandable and easy to read experience when using
syntax highlighting in editors.


Line Statements
~~~~~~~~~~~~~~~

Line statements can be utilized by using the ``%%`` tag:

.. code-block::

    %% if 10 > 7
        it is bigger
    %% else
        it is smaller
    %% endif



Block Statements
~~~~~~~~~~~~~~~~

Blocks begin with a ``\BLOCK{`` and ends with a ``}``.

Blocks can be used in the following manner:

.. code-block::

    \BLOCK{
        set some_var = "some value"
    }



Using Variables
~~~~~~~~~~~~~~~

Variables are output by using ``\VAR{`` which ends in ``}``:

.. code-block::

    \VAR{ some_var }

However when outputting text it is **strongly** recommended to always escape using the ``escape`` or ``e`` filter:

.. code-block::

    \VAR{ some_var | escape }

or the short harder to read version:

.. code-block::

    \VAR{ somevar | e }



Single Line Comments
~~~~~~~~~~~~~~~~~~~~

Single line comments can be made using the ``%#`` line statement:

.. code-block::

    %# Hello World



Block Comments
~~~~~~~~~~~~~~

Block comments can be made by using ``\#{`` ending in ``}``:

.. code-block::

    \#{
        This is a
        comment block.
    }


Jinja2 Syntax For HTML
----------------------

Docplates uses normal Jinja2 syntax for HTML templates.



Builtin Globals
---------------

Jinja2 globals are supported and can be found here `Jinja2 Functions`_.

.. _Jinja2 Functions: https://jinja.palletsprojects.com/en/latest/templates/#list-of-global-functions


DOCUMENT_NAME: str
    This is the resulting document file name. This is not the full path, it is only the last component of the path.


data: Any
    The ``data`` global contains data loaded using the command line option ``--load-data``.


log_debug(message: str)
    The ``log_debug`` function is used to log information which will be visible as ``TEMPLATE_LOG`` messages when using the
    ``--verbose`` command line option. The output level for ``log_debug`` is ``DEBUG``.

    Here is an example for LaTex:

    .. code-block::

        %% do log_debug("Hello world")

    Here is an example for HTML:

    .. code-block:: jinja

        # do log_debug("hello world")


log_info(message: str)
    The ``log_info`` function is used to log information which would be visible as ``TEMPLATE_LOG`` messages. The output level for
    ``log_info`` is ``INFO``.

    Here is an example for LaTex:

    .. code-block::

        %% do log_info("Hello world")

    Here is an example for HTML:

    .. code-block:: jinja

        # do log_info("hello world")


log_warning(message: str)
    The ``log_warning`` function is used to log information which would be visible as ``TEMPLATE_LOG`` messages. The output level
    for ``log_warning`` is ``WARNING``.

    Here is an example for LaTex:

    .. code-block::

        %% do log_warning("Hello world")

    Here is an example for HTML:

    .. code-block:: jinja

        # do log_warning("hello world")


log_error(message: str)
    The ``log_error`` function is used to log information which would be visible as ``TEMPLATE_LOG`` messages. The output level for
    ``log_error`` is ``ERROR``.

    Here is an example for LaTex:

    .. code-block::

        %% do log_error("Hello world")

    Here is an example for HTML:

    .. code-block:: jinja

        # do log_error("hello world")


datetime
    The ``datetime`` global is a direct import of the Python ``datetime`` module and can be used to perform datetime parsing and
    calculations.

    Here is an example for LaTeX:

    .. code-block::

        %% set date_now = datetime.utcnow().strftime("%Y-%m-%d")

    Here is an example for HTML:

    .. code-block:: jinja

        # set date_now = datetime.utcnow().strftime("%Y-%m-%d")


debug(message: str)
    The ``debug`` function is used to dump the current template environment, it would be logged as a debug level message requring
    the use of ``--verbose``.

    Here is an example for LaTeX:

    .. code-block::

        %% do debug()

    Here is an example for HTML:

    .. code-block:: jinja

        # do debug()



export(name: str, value: Any)
    The ``export`` function is used to export a variable from the template, this can then be picked up by using ``--export`` and
    ``--export-format``.

    Here is an example for LaTeX:

    .. code-block::

        %% do export("somevar", "somevalue")

    Here is an example for HTML:

    .. code-block:: jinja

        # do export("somevar", "somevalue")

    It is important to note that subsequent calls to ``export`` will result in the exported variable value being replaced. Any
    flat data structure can be exported including strings, numbers, dicts and lists.


raise(message: str)
    The ``raise`` function raises an exception from within a template.

    Here is an example for LaTeX:

    .. code-block::

        %% do raise("This is an exception")

    Here is an example for HTML:

    .. code-block:: jinja

        # do raise("This is an exception")


timedelta
    The ``timedelta`` global is a direct import from the Python ``timedelta`` module and can be used to perform datetime calculations.

    Here is an example for LaTeX:

    .. code-block::

        %% set date_next_month = (datetime.utcnow() + timedelta(months=1)).strftime("%Y-%m-%d")

    Here is an example for HTML:

    .. code-block:: jinja

        # set date_next_month = (datetime.utcnow() + timedelta(months=1)).strftime("%Y-%m-%d")


use_resource(strip_extension: bool, render: bool)
    The `use_resource` function can be used when including images in order to copy that resource into the document builder path
    during PDF creation. It can also be used with HTML templates in order to parse CSS stylesheets.

    Here is an example using this in LaTex in order to include graphics can be found here:

    .. code-block::

        \includegraphics{\VAR{ use_resource("branding/images/mylogo.pdf", strip_extension=true) }}

    And an example of using this with HTML and CSS stylesheets can be found here:

    .. code-block:: jinja

        <head>
            <meta charset="utf-8">
            <link href="{{ use_resource('ticket.css', render=true) }}" rel="stylesheet">
            <title>Boarding ticket</title>
            <meta name="description" content="Boarding ticket">
        </head>

        ...

        @font-face {
            font-family: Barlow Condensed;
            font-weight: 300;
            src: url({{ use_resource("fonts/barlowcondensed-light.otf") }});
        }

    .. _use_resource:


Builtin Filters
---------------

Jinja2 filters are supported and can be found here `Jinja2 Filters`_.

.. _Jinja2 Filters: https://jinja.palletsprojects.com/en/latest/templates/#list-of-builtin-filters

parse_yaml
    The ``parse_yaml`` filter can be used to parse a block of YAML into a datastructure which can be assigned to a variable.

    This can be used to pass data to other functions or addons.

    One can do this using LaTex by following the example below:

    .. code-block::

        \BLOCK{ set somevar | parse_yaml }
        some: thing
        hello: world
        somelist:
            - item1
            - item2
        \BLOCK{ endset }

    or in HTML using this example:

    .. code-block:: jinja

        {% set somevar | parse_yaml %}
        some: thing
        hello: world
        somelist:
            - item1
            - item2
        {% endset %}


    The variable ``somevar`` would now contain the above structure.



Using Templates From Addons
---------------------------

Templates provided by addons can be used by prefixing them with a ``lib/``. For instance if an addon implements a
``helloworld.tex`` template, one would use this by using ``lib/helloworld.tex``.
