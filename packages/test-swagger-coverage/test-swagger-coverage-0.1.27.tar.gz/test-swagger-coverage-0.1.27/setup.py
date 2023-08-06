# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swagger_coverage', 'swagger_coverage.scripts']

package_data = \
{'': ['*'], 'swagger_coverage': ['src/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'attrs>=21.4.0,<22.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['swagger_coverage = '
                     'swagger_coverage.scripts.swagger_report:main']}

setup_kwargs = {
    'name': 'test-swagger-coverage',
    'version': '0.1.27',
    'description': 'Swagger coverage for API tests',
    'long_description': None,
    'author': 'alexanderlozovoy',
    'author_email': 'berpress@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
