# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['group4package', 'group4package..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'matplotlib==3.5.1',
 'numpy==1.21.5',
 'pandas>=1.4.2',
 'pandoc>=2.1,<3.0',
 'plotly>=5.6.0,<6.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'group4package',
    'version': '0.1.2',
    'description': "Package containing functions to run Group 4's Data Analysis",
    'long_description': "# group4package\n\nA package for running Group 4's data analysis\n\n## Installation\n\n```bash\n$ pip install group4package\n```\n\n## Usage\n\n- group 4 package can be used for the following parts of a data analysis:\n- produce a count plot\n- calculate summary statistics\n- calculate classification metrics\n- pre-process data \n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`group4package` was created by Hannah, Jordan, Diana, and Shravan. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`group4package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Hannah, Diana, Jordan, Shravan ',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
