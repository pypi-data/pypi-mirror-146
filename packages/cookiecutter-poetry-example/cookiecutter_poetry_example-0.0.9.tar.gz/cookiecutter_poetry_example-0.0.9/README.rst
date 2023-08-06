==================================
cookiecutter-poetry-example
==================================

.. image:: https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example
	:target: https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example
	:alt: Release

.. image:: https://img.shields.io/github/workflow/status/fpgmaas/cookiecutter-poetry-example/merge-to-main
	:target: https://img.shields.io/github/workflow/status/fpgmaas/cookiecutter-poetry-example/merge-to-main
	:alt: Build status

.. image:: https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example
    :target: https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example
    :alt: Commit activity

.. image:: https://img.shields.io/badge/docs-gh--pages-blue
    :target: https://fpgmaas.github.io/cookiecutter-poetry-example/
    :alt: Docs

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
	:target: https://github.com/psf/black
	:alt: Code style with black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1
	:target: https://pycqa.github.io/isort/
	:alt: Imports with isort

.. image:: https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example
	:target: https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example
	:alt: License

This is a template repository for Python projects that use Poetry for their dependency management.

* **Github repository**: `https://github.com/fpgmaas/cookiecutter-poetry-example/ <https://github.com/fpgmaas/cookiecutter-poetry-example/>`_
* **Documentation**: `https://fpgmaas.github.io/cookiecutter-poetry-example/ <https://fpgmaas.github.io/cookiecutter-poetry-example/>`_


Releasing a new version
-----------------------------

- Create an API Token on `Pypi <https://pypi.org/>`_
- Add the API Token to your projects secrets with the name ``PYPI_TOKEN`` by visiting `this page <https://github.com/fpgmaas/cookiecutter-poetry-example/settings/secrets/actions/new>`_.
- Create a `new release <https://github.com/fpgmaas/cookiecutter-poetry-example/releases/new>`_ on Github. Create a new tag in the form ``*.*.*``.

For more details, see `here <https://fpgmaas.github.io/cookiecutter-poetry/releasing.html>`_.

---------

Repository initiated with `fpgmaas/cookiecutter-poetry <https://github.com/fpgmaas/cookiecutter-poetry>`_