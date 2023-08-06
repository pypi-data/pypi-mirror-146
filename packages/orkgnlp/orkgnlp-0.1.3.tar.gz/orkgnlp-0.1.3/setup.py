# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orkgnlp', 'orkgnlp.util']

package_data = \
{'': ['*']}

install_requires = \
['huggingface-hub>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'orkgnlp',
    'version': '0.1.3',
    'description': 'Python package wrapping the ORKG NLP Services.',
    'long_description': '# ORKG NLP PyPI\n[![Documentation Status](https://readthedocs.org/projects/orkg-nlp-pypi/badge/?version=latest)](https://orkg-nlp-pypi.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/orkgnlp.svg)](https://badge.fury.io/py/orkgnlp)\n\nPyPI package wrapping the ORKG NLP services.\n\nCheck our [Read the Docs](https://orkg-nlp-pypi.readthedocs.io/en/latest/) for more details!',
    'author': 'Omar Arab Oghli',
    'author_email': 'omar.araboghli@outlook.com',
    'maintainer': 'Omar Arab Oghli',
    'maintainer_email': None,
    'url': 'http://orkg.org/about',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
