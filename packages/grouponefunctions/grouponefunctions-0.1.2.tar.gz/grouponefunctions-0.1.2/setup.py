# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grouponefunctions']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1', 'numpy==1.21.5', 'pandas>=1.4.2']

setup_kwargs = {
    'name': 'grouponefunctions',
    'version': '0.1.2',
    'description': 'A package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1',
    'long_description': '# grouponefunctions\n\nA package containing the necessary functions to smoothly run the analysis in DSCI-310-Group-1\n\n## Installation\n\n```bash\n$ pip install grouponefunctions\n```\n\n## Usage\n\n- The package has three functions: splitxy, listfun, and plotsquaredata.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`grouponefunctions` was created by Andres Zepeda Perez, Daniel Hou, Zizhen Guo, Timothy Zhou. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`grouponefunctions` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Andres Perez, Daniel Hou, Zizhen Guo, Timothy Zhou',
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
