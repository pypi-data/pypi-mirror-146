# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twita']

package_data = \
{'': ['*']}

install_requires = \
['aiometer>=0.3.0', 'httpx[socks,http2]>=0.21.0']

setup_kwargs = {
    'name': 'twita',
    'version': '0.0.2',
    'description': 'Twitter Hidden API Library',
    'long_description': '# Twita\n\n> **WIP**\n\nA library to fetch Twitter data using Twitter API v2 (hidden).\n\n<!-- [![Latest Version](https://img.shields.io/pypi/v/twita.svg)](https://pypi.python.org/pypi/twita)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/twita)](https://pypi.python.org/pypi/twita)\n[![CI](https://github.com/countertek/twita/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/countertek/twita/actions/workflows/ci.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub license](https://img.shields.io/github/license/countertek/twita)](https://github.com/countertek/twita/blob/main/LICENSE) -->\n\n<!-- **[Documentation](https://countertek.github.io/twita)**\n**·**\n**[Replit Playground](https://replit.com/@darekaze/twita-examples#main.py)** -->\n\n## Why this library?\n\n> To be filled.\n\n**twita** tries to counter these problems to provide these features:\n\n- No authentication (API key) is needed to access the data.\n- Fully Async based.\n- Proxy support via [httpx](https://www.python-httpx.org/advanced/#http-proxying).\n\n## Install\n\nYou can install this library easily from pypi:\n\n```bash\n# with pip\npip install twita\n\n# with poetry\npoetry add twita\n```\n\n## License\n\n[![GNU LGPLv3 Image](https://www.gnu.org/graphics/lgplv3-147x51.png)](https://www.gnu.org/licenses/lgpl-3.0.html)\n\nCopyright (C) 2022-present DaRekaze \\<https://github.com/darekaze>\n\nTwita is free software: you can redistribute it and/or modify\nit under the terms of the GNU Lesser General Public License as published\nby the Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nTwita is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Lesser General Public License for more details.\n\nYou should have received a copy of the GNU Lesser General Public License\nalong with Twita. If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'DaRekaze',
    'author_email': 'darekaze@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CounterTek/twita',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
