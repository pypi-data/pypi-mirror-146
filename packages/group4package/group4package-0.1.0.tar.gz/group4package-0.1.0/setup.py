# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['group4package', 'group4package..ipynb_checkpoints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'group4package',
    'version': '0.1.0',
    'description': 'A package for doing great things!',
    'long_description': '# group4package\n\nA package for doing great things!\n\n## Installation\n\n```bash\n$ pip install group4package\n```\n\n## Usage\n\n- group 4 package can be used for the following parts of a data analysis:\n- produce a count plot\n- calculate summary statistics\n- calculate classification metrics\n- pre-process data \n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`group4package` was created by Hannah, Jordan, Diana, and Shravan. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`group4package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Hannah Martin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
