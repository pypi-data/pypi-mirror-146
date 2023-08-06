# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coverage_plot']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'click>=8.1.2,<9.0.0',
 'pandas>=1.0.5,<2.0.0',
 'plotly>=4.8.2,<5.0.0',
 'pydriller>=1.15.2,<2.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4']}

entry_points = \
{'console_scripts': ['coverage-plot = coverage_plot.cli:coverage_plot']}

setup_kwargs = {
    'name': 'coverage-plot',
    'version': '0.2.0',
    'description': 'Library to plot Python code coverage results',
    'long_description': '# Coverage Plot\n\n[![codecov](https://codecov.io/gh/imankulov/coverage-plot/branch/master/graph/badge.svg)](https://codecov.io/gh/imankulov/coverage-plot)\n[![Coverage Status](https://coveralls.io/repos/github/imankulov/coverage-plot/badge.svg)](https://coveralls.io/github/imankulov/coverage-plot)\n[![Maintainability](https://api.codeclimate.com/v1/badges/0f758ae06864812dce12/maintainability)](https://codeclimate.com/github/imankulov/coverage-plot/maintainability)\n[![Documentation Status](https://readthedocs.org/projects/coverage-plot/badge/?version=latest)](https://coverage-plot.readthedocs.io/en/latest/?badge=latest)\n\nA library and a script to plot Python code coverage results.\n\n## Getting Started\n\nRun the tests for your project with the test coverage, and convert the coverage results to a JSON or XML format. As a result, you shoud find a coverage.json or coverage.xml file in your current working directory.\n\n```\ncoverage run pytest\ncoverage xml  # or coverage json\n```\n\nInstall the package.\n\n```\npip install coverage-plot\n```\n\nRun the coverage visualization. The script opens the browser with the visualization-results.\n\n```\ncoverage-plot coverage.xml\n```\n',
    'author': 'Roman Imankulov',
    'author_email': 'roman.imankulov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imankulov/coverage-plot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
