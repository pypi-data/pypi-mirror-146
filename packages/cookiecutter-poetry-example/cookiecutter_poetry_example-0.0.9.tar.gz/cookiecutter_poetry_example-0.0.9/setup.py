# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cookiecutter_poetry_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cookiecutter-poetry-example',
    'version': '0.0.9',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '==================================\ncookiecutter-poetry-example\n==================================\n\n.. image:: https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example\n\t:target: https://img.shields.io/github/v/release/fpgmaas/cookiecutter-poetry-example\n\t:alt: Release\n\n.. image:: https://img.shields.io/github/workflow/status/fpgmaas/cookiecutter-poetry-example/merge-to-main\n\t:target: https://img.shields.io/github/workflow/status/fpgmaas/cookiecutter-poetry-example/merge-to-main\n\t:alt: Build status\n\n.. image:: https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example\n    :target: https://img.shields.io/github/commit-activity/m/fpgmaas/cookiecutter-poetry-example\n    :alt: Commit activity\n\n.. image:: https://img.shields.io/badge/docs-gh--pages-blue\n    :target: https://fpgmaas.github.io/cookiecutter-poetry-example/\n    :alt: Docs\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n\t:target: https://github.com/psf/black\n\t:alt: Code style with black\n\n.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1\n\t:target: https://pycqa.github.io/isort/\n\t:alt: Imports with isort\n\n.. image:: https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example\n\t:target: https://img.shields.io/github/license/fpgmaas/cookiecutter-poetry-example\n\t:alt: License\n\nThis is a template repository for Python projects that use Poetry for their dependency management.\n\n* **Github repository**: `https://github.com/fpgmaas/cookiecutter-poetry-example/ <https://github.com/fpgmaas/cookiecutter-poetry-example/>`_\n* **Documentation**: `https://fpgmaas.github.io/cookiecutter-poetry-example/ <https://fpgmaas.github.io/cookiecutter-poetry-example/>`_\n\n\nReleasing a new version\n-----------------------------\n\n- Create an API Token on `Pypi <https://pypi.org/>`_\n- Add the API Token to your projects secrets with the name ``PYPI_TOKEN`` by visiting `this page <https://github.com/fpgmaas/cookiecutter-poetry-example/settings/secrets/actions/new>`_.\n- Create a `new release <https://github.com/fpgmaas/cookiecutter-poetry-example/releases/new>`_ on Github. Create a new tag in the form ``*.*.*``.\n\nFor more details, see `here <https://fpgmaas.github.io/cookiecutter-poetry/releasing.html>`_.\n\n---------\n\nRepository initiated with `fpgmaas/cookiecutter-poetry <https://github.com/fpgmaas/cookiecutter-poetry>`_',
    'author': 'Florian Maas',
    'author_email': 'ffpgmaas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fpgmaas/cookiecutter-poetry-example',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
