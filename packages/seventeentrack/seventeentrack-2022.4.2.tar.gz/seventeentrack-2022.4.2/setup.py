# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seventeentrack',
 'seventeentrack.data',
 'seventeentrack.legacy',
 'seventeentrack.v1']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0', 'attrs>=19.3', 'pytz>=2021.1']

setup_kwargs = {
    'name': 'seventeentrack',
    'version': '2022.4.2',
    'description': 'A Simple Python API for 17track.net',
    'long_description': '# 📦 seventeentrack: A Simple Python API for 17track.net\n\n[![CI](https://github.com/mcswindler/seventeentrack/workflows/CI/badge.svg)](https://github.com/mcswindler/seventeentrack/actions)\n[![PyPi](https://img.shields.io/pypi/v/seventeentrack.svg)](https://pypi.python.org/pypi/seventeentrack)\n[![Version](https://img.shields.io/pypi/pyversions/seventeentrack.svg)](https://pypi.python.org/pypi/seventeentrack)\n[![License](https://img.shields.io/pypi/l/seventeentrack.svg)](https://github.com/mcswindler/seventeentrack/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/mcswindler/seventeentrack/branch/master/graph/badge.svg)](https://codecov.io/gh/mcswindler/seventeentrack)\n[![Maintainability](https://api.codeclimate.com/v1/badges/cd4e8b7fcc8f840009e5/maintainability)](https://codeclimate.com/github/mcswindler/seventeentrack/maintainability)\n\n`seventeentrack` is a simple Python library to track packages in\n[17track.net](http://www.17track.net/) accounts.\n\nThis project was built off of [py17track](https://github.com/bachya/py17track).\n\n## V1 API\n\nYou can register an account first here: https://features.17track.net/en/api\nEach account will have 100 free tracking quota for testing.\nOnce logged in, you can find the API token/Access key under Settings -> Security -> Access Key\n\n# Python Versions\n\n`seventeentrack` is currently supported on:\n\n- Python 3.7\n- Python 3.8\n- Python 3.9\n- Python 3.10\n\n# Installation\n\n```python\npip install seventeentrack\n```\n\n# Usage\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom seventeentrack import Client, Version\n\n\nasync def main() -> None:\n    """Run!"""\n    client = Client(version=Version.V1)\n\n    # Login with API token:\n    client.profile.login("<TOKEN>")\n\n    # Get a summary of the user\'s packages:\n    summary = await client.profile.summary()\n    # >>> {\'In Transit\': 3, \'Expired\': 3, ... }\n\n    # Get all packages associated with a user\'s account:\n    packages = await client.profile.packages()\n    # >>> [seventeentrack.package.Package(..), ...]\n\n    # Add new packages by tracking number\n    await client.profile.add_package(\'<TRACKING NUMBER>\', \'<FRIENDLY NAME>\')\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\nBy default, the library creates a new connection to 17track with each coroutine. If you\nare calling a large number of coroutines (or merely want to squeeze out every second of\nruntime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom seventeentrack import Client\n\n\nasync def main() -> None:\n    """Run!"""\n    async with ClientSession() as session:\n        client = Client(session=session)\n\n        # ...\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\n\nEach `Package` object has the following info:\n\n- `destination_country`: the country the package was shipped to\n- `friendly_name`: the human-friendly name of the package\n- `info`: a text description of the latest status\n- `location`: the current location (if known)\n- `timestamp`: the timestamp of the latest event\n- `origin_country`: the country the package was shipped from\n- `package_type`: the type of package (if known)\n- `status`: the overall package status ("In Transit", "Delivered", etc.)\n- `tracking_info_language`: the language of the tracking info\n- `tracking_number`: the all-important tracking number\n- `carrier`: the logistics company transporting the package\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/mcswindler/seventeentrack/issues)\n   or [initiate a discussion on one](https://github.com/mcswindler/seventeentrack/issues/new).\n2. [Fork the repository](https://github.com/mcswindler/seventeentrack/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n\n# Updating Carrier and Country JSON\n\nIf the carrier or country lists need to be updated to support new ones, simply download the updated JSON from 17track.\n\nhttps://res.17track.net/asset/carrier/info/carrier.all.json\n\nhttps://res.17track.net/asset/carrier/info/country.all.json\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcswindler/seventeentrack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
