# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_plugin_helper', 'mc_plugin_helper.file_manager']

package_data = \
{'': ['*']}

install_requires = \
['click==8.0.4', 'pyyaml==6.0']

extras_require = \
{'docs': ['sphinx>=4.5,<5.0',
          'sphinx-autodoc-typehints>=1.17,<2.0',
          'sphinxcontrib-apidoc>=0.3,<0.4',
          'furo',
          'm2r2>=0.3,<0.4',
          'tomlkit>=0.10,<0.11',
          'toml>=0.10,<0.11']}

entry_points = \
{'console_scripts': ['mc-plugin-helper = mc_plugin_helper.__main__:run']}

setup_kwargs = {
    'name': 'mc-plugin-helper',
    'version': '0.1.0b0',
    'description': 'Minecraft plugin helper, updates and checks versions of all plugins on a server!',
    'long_description': '# mc-plugin-helper\n\n[![Build Status](https://github.com/PerchunPak/mc-plugin-helper/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/mc-plugin-helper/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/PerchunPak/mc-plugin-helper/branch/master/graph/badge.svg)](https://codecov.io/gh/PerchunPak/mc-plugin-helper)\n[![Documentation Build Status](https://readthedocs.org/projects/mc-plugin-helper/badge/?version=latest)](https://mc-plugin-helper.readthedocs.io/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Python Version](https://img.shields.io/pypi/pyversions/mc-plugin-helper.svg)](https://pypi.org/project/mc-plugin-helper/)\n\nMinecraft plugin helper, updates and checks versions of all plugins on a server!\n\n# Project in developing! Please do not use it!\n\nAt now implemented only output of plugins names.\n\n## Features\n\n- Nice and powerful [documentation](https://mc-plugin-helper.readthedocs.io/en/latest/)!\n- Easy management plugins in simple commands!\n- Easy readable and supportable code!\n- Support for Spigot.org plugins!\n\n\n## Installation\n\n```bash\npip install mc-plugin-helper\n```\n\n\n## Example\n\nCheck updates for all plugins:\n\n```bash\n> mc-plugin-helper check all .\n\nPlugin: AuthMe\nPlugin: ClearLag\nPlugin: CMI\nPlugin: CMILib\nPlugin: CoreProtect\nPlugin: FastAsyncWorldEdit\nPlugin: Geyser-Spigot\nPlugin: LuckPerms\n```\n\n## Thanks\n\n## Credits\n\nThis project was generated with [`autodonate-plugin-template`](https://github.com/fire-squad/autodonate-plugin-template). \nCurrent template version is: [cc64ede4f27ca8e272bff0a42d3950d26bcacb9a](https://github.com/fire-squad/autodonate-plugin-template/tree/cc64ede4f27ca8e272bff0a42d3950d26bcacb9a). \nSee what is [updated](https://github.com/fire-squad/autodonate-plugin-template/compare/cc64ede4f27ca8e272bff0a42d3950d26bcacb9a...master) \nsince then.\n',
    'author': 'PerchunPak',
    'author_email': 'perchunpak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PerchunPak/mc-plugin-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
