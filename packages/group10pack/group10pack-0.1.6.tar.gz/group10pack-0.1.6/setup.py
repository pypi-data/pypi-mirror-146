# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['group10pack']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.5.0,<5.0.0',
 'docopt>=0.6.2,<0.7.0',
 'jupyterlab>=3.3.3,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pytest>=7.1.1,<8.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'group10pack',
    'version': '0.1.6',
    'description': 'This package contains the functions for the Statistics Canada investment income analysis,by group 10',
    'long_description': '# DSCI-310-Group-10-Package\n\nDSCI-310-Group-10-Package is a Python package for the investment income outcome analysis done for DSCI310. This package is largely dependent on the scikit-learn and matplotlib packages, and is distributed under the MIT License.\n\nThe functions in this package have roles related to hyperparamater optimizations for specific machine learning models, and plot the results obtained.\n\nThe main project where this package is used can be found in the following GitHub Repository: https://github.com/DSCI-310/DSCI-310-Group-10\n\n## Installation\n\n```bash\n$ pip install group10pack\n```\n\n## Usage\n\n- [example](docs/example.ipynb)\n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`DSCI-310-Group-10-Package` was created by Harry Zhang Ahmed Rizk Mahdi Heydar Nikko Dumrique. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`DSCI-310-Group-10-Package` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Harry Zhang Ahmed Rizk Mahdi Heydar Nikko Dumrique',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
