# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricks_cdk']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.10,<2.0.0',
 'cfnresponse>=1.1.2,<2.0.0',
 'pydantic>=1.4.0,<2.0.0',
 'requests>=2.22']

setup_kwargs = {
    'name': 'databricks-cdk',
    'version': '0.1.0',
    'description': 'Deploying databricks resources from cdk',
    'long_description': '',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/godatadriven/databricks-cdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
