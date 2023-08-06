# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_cargo']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.20.49,<2.0.0',
 'mkdocs-git-revision-date-plugin>=0.3.1,<0.4.0',
 'mkdocs-material>7.3',
 'mkdocs>=1.2.3,<2.0.0',
 'mkdocstrings>0.16.0',
 'patool>=1.12,<2.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyunpack>=0.2.2,<0.3.0']

extras_require = \
{'dev_tools': ['pudb>=2022.1,<2023.0']}

setup_kwargs = {
    'name': 's3-cargo',
    'version': '2022.2',
    'description': 'Manage your projects in S3 buckets.',
    'long_description': None,
    'author': 'MONTANA Knowledge Management ltd.',
    'author_email': 'info@distiller.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
