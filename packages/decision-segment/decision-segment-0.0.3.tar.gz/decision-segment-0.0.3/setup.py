# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decision_segment']

package_data = \
{'': ['*']}

install_requires = \
['citation-decision>=0.0.3,<0.0.4',
 'decision-footnote>=0.0.1,<0.0.2',
 'decision-section>=0.0.1,<0.0.2',
 'decision-title>=0.0.2,<0.0.3',
 'statute-matcher>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'decision-segment',
    'version': '0.0.3',
    'description': 'Separates decision segments',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
