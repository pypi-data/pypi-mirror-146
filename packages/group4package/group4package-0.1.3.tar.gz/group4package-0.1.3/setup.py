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
    'version': '0.1.3',
    'description': "Package containing functions to run Group 4's Data Analysis",
    'long_description': '# group4package\n\nA package for running Group 4\'s data analysis\n\n## Installation\n\n*Note: This package requires python version 3.9.1 or greater*\n\n```bash\n$ pip install group4package\n```\n\n## Usage\n\nThe following functions in this package were created for Group 4\'s Project [Predicting Defaults of Credit Card Clients](https://github.com/DSCI-310/DSCI-310-Group-4). \nHowever, they are useful for any data analysis that involves pre-processing data and calculating classification metrics and statistics. \n\n**`calculate_metrics(FP, TN, TP)`**\n-  calulates Recall, F1-Score and Precision for a classification model \n\nExample:\n\n```python \nfrom group4package import metrics_function as cm\nTN, FP, FN, TP = confusion_matrix(y_test, predict).ravel()\nres = cm.calculate_metrics(FP, FN, TP)\n```\n \n**`get_summary_stats(df)`**\n- calculates summary statistics including mean, std, min, and max of numeric columns of a dataframe\n\nExample:\n\n```python \nfrom group4package import summary_stats_function as ss\nss.get_summary_stats(train_df)\n```\n\n**`count_plot(df, x, name)`**\n- creates a plot of the counts between x and y values of the given dataframe, while the latter two arguments are used as the x-axis label and title of the produced plot\n\nExample:\n\n```python \nfrom group4package.function_count_plot import count_plot\nnew_plot = count_plot(df=train_df, x="x-axis label", name="Plot Title")\n```\n\n**`pre-process data(df, train_frac, seed)`**\n- drops all rows with missing or null values and then splits the dataframe into training and testing sets according to the given split ratio\n\nExample:\n\n```python \nfrom group4package import preprocess as pp\ntrain_df, test_df = pp.preprocess(df, 0.8, 200)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`group4package` was created by Hannah, Jordan, Diana, and Shravan. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`group4package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
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
