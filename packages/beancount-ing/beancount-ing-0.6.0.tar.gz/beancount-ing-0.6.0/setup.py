# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_ing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beancount-ing',
    'version': '0.6.0',
    'description': 'Beancount Importer for ING (DE) CSV exports',
    'long_description': "# Beancount ING-DiBa Importer\n\n[![image](https://github.com/siddhantgoel/beancount-ing/workflows/beancount-ing/badge.svg)](https://github.com/siddhantgoel/beancount-ing/workflows/beancount-ing/badge.svg)\n\n[![image](https://img.shields.io/pypi/v/beancount-ing.svg)](https://pypi.python.org/pypi/beancount-ing)\n\n[![image](https://img.shields.io/pypi/pyversions/beancount-ing.svg)](https://pypi.python.org/pypi/beancount-ing)\n\n[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`beancount-ing` provides an Importer for converting CSV exports of\n[ING-DiBa] (Germany) account summaries to the [Beancount] format.\n\n## Installation\n\n```sh\n$ pip install beancount-ing\n```\n\nIn case you prefer installing from the Github repository, please note that\n`develop` is the development branch so `stable` is what you should be installing\nfrom.\n\n## Usage\n\nIf you're not familiar with how to import external data into Beancount, please\nread [this guide] first.\n\nAdjust your [config file] to include the provided `ECImporter`. A sample\nconfiguration might look like the following:\n\n```python\nfrom beancount_ing import ECImporter\n\nCONFIG = [\n    # ...\n\n    ECImporter(\n        IBAN_NUMBER,\n        'Assets:INGDiBa:EC',\n        'Max Mustermann',\n        file_encoding='ISO-8859-1',\n    ),\n\n    # ...\n]\n```\n\nOnce this is in place, you should be able to run `bean-extract` on the command\nline to extract the transactions and pipe all of them into your Beancount file.\n\n```sh\n$ bean-extract /path/to/config.py transaction.csv >> you.beancount\n```\n\n## Contributing\n\nContributions are most welcome!\n\nPlease make sure you have Python 3.6+ and [Poetry] installed.\n\n1. Clone the repository: `git clone https://github.com/siddhantgoel/beancount-ing`\n2. Install the packages required for development: `poetry install`\n3. That's basically it. You should now be able to run the test suite: `poetry\n   run pytest tests/`.\n\n[Beancount]: http://furius.ca/beancount/\n[config file]: https://beancount.github.io/docs/importing_external_data.html#configuration\n[ING-DiBa]: https://www.ing.de/\n[Poetry]: https://python-poetry.org/\n[this guide]: https://beancount.github.io/docs/importing_external_data.html\n",
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/siddhantgoel/beancount-ing',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
