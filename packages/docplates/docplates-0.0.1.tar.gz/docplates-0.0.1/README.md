[![pipeline status](https://gitlab.oscdev.io/software/docplates/docplates/badges/main/pipeline.svg)](https://gitlab.oscdev.io/software/docplates/docplates/commits/main)
[![coverage report](https://gitlab.oscdev.io/software/docplates/docplates/badges/main/coverage.svg)](https://gitlab.oscdev.io/software/docplates/docplates/commits/main)

# Docplates

Docplates is a PDF document templater which uses Jinja2 and LaTeX/WeasyPrint backends to create documents.


# Installing

Docplates can be simply installed by running:

    pip install docplates

Or if you prefer the development branch, one could use:

    pip install git+https://gitlab.oscdev.io/software/docplates/docplates.git

Alternatively if you prefer installing from a checked out git repository:

    pip install .

Lastly, you could also build it and install the wheel...

    tox -e build
    pip install dist/docplates-*.whl


# Documentation

  * [Docplates Documentation](https://software.pages.oscdev.io/docplates/docplates)
  * [Contributing](https://gitlab.oscdev.io/oscdev/contributing/-/blob/master/README.md)

# Support

  * [Issue Tracker](https://gitlab.oscdev.io/software/docplates/docplates/-/issues)


# License

Docplates is licensed under the [GNU GPL v3 License](LICENSE).
