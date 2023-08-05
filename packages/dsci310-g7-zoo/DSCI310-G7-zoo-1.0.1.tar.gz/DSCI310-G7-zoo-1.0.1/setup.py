# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zoo']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pytest>=7.0.1,<8.0.0',
 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'dsci310-g7-zoo',
    'version': '1.0.1',
    'description': 'Package created for dsci_310 zoo analysis',
    'long_description': '# zoo\n\nPackage created for dsci_310 zoo analysis\n\n## Installation\n\n```bash\n$ pip install zoo\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`zoo` was created by Group_7. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`zoo` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Group_7',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
