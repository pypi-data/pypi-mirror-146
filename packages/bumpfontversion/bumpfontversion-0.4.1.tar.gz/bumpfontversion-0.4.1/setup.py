# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumpfontversion']

package_data = \
{'': ['*']}

install_requires = \
['bump2version==1.0.1',
 'fontTools',
 'glyphsLib>=6,<7',
 'openstep-plist',
 'ufoLib2']

entry_points = \
{'console_scripts': ['bumpfontversion = bumpfontversion:main']}

setup_kwargs = {
    'name': 'bumpfontversion',
    'version': '0.4.1',
    'description': 'Bumps the version of a font source file',
    'long_description': '# bumpfontversion\n\nVersion-bump your *source* font files.\n\nThis tool, patterned after the wonderful [bumpversion](https://github.com/c4urself/bump2version), allows you to update the version of your font source files, as well as create commits and tags in git.\n\nIt currently supports UFO and Glyphs format font files.\n\n## Installation\n\nYou can download and install the latest version of this software from the Python package index (PyPI) as follows:\n\n````\npip install --upgrade bumpfontversion\n```\n\n## Usage\n\nFor users of bump2version, please note that the interface is slightly different. You can *either* use:\n\n```\nbumpfontversion --new-version 0.5 MyFont.ufo\n```\n\nto set the version directly, or\n\n```\nbumpfontversion --part minor MyFont.glyphs # Upgrade the minor version\nbumpfontversion --part major MyFont.glyphs # Upgrade the major version\n```\n\nAs per bump2version, you can use `--commit` to commit the new version to git, and `--tag` to add a new git tag.\n\n## See also\n\n* [bumpversion](https://github.com/c4urself/bump2version)\n* [font-v](https://github.com/source-foundry/font-v): Similar tool for font *binary* files\n\n## License\n\n[Apache license](http://www.apache.org/licenses/LICENSE-2.0)\n',
    'author': 'Simon Cozens',
    'author_email': 'simon@simon-cozens.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
