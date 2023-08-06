# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['example_package_lth']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.15.0,<4.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['example-package-lth = example_package_lth.console:main']}

setup_kwargs = {
    'name': 'example-package-lth',
    'version': '0.1.0',
    'description': 'An example Python package',
    'long_description': '# Python Example Package\n[![Tests](https://github.com/letuanhai/python-example-package-lth/workflows/Tests/badge.svg)](https://github.com/letuanhai/python-example-package-lth/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/letuanhai/python-example-package-lth/branch/master/graph/badge.svg)](https://codecov.io/gh/letuanhai/python-example-package-lth)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python.svg)](https://pypi.org/project/letuanhai/python-example-package-lth/)\n\nClone of cjolowicz/hypermodern-python\n\nMaking an example package using *modern* Python toolchain.\nTo quick start with a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template, refer to [https://github.com/cjolowicz/cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python).\n\nTopics covered:\n- Create a package in *src* layout\n- Manage dependency with *Poetry*\n- Command-line interfaces with *click*\n- Consume a REST API with *requests*\n- Unit testing with *pytest*\n- Code coverage with *Coverage.py*\n- Test automation with *Nox*\n- Mocking with *pytest-mock*\n- End-to-end testing\n- Linting with *flake8*\n- Code formatting with *black*\n- Checking import with *flake8-import-order*\n- Finding more bugs with *flake8-bugbear*\n- Identifying security issues with *bandit*\n- Finding security vulnerabilities in dependencies with *Safety*\n- Managing dependencies in *Nox* sessions with *Poetry*\n- Managing Git hooks with *pre-commit*\n',
    'author': 'letuanhai',
    'author_email': 'letuanhai@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/letuanhai/python-example-package-lth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
