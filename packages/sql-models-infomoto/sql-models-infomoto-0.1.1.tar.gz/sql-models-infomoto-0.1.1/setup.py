# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_models',
 'sql_models.manufacturer',
 'sql_models.motorcycle_model',
 'sql_models.motorcycle_model.sections',
 'sql_models.motorcycle_model.sections.abs',
 'sql_models.motorcycle_model.sections.autodiagnosis',
 'sql_models.motorcycle_model.sections.components',
 'sql_models.motorcycle_model.sections.custom_electrical_scheme',
 'sql_models.motorcycle_model.sections.distribution',
 'sql_models.motorcycle_model.sections.electronic',
 'sql_models.motorcycle_model.sections.engine',
 'sql_models.motorcycle_model.sections.frame',
 'sql_models.motorcycle_model.sections.generic_replacements',
 'sql_models.motorcycle_model.sections.hiss_immobilizer',
 'sql_models.motorcycle_model.sections.power_supply',
 'sql_models.motorcycle_model.sections.smart_key',
 'sql_models.motorcycle_model.sections.tightening_specifications',
 'sql_models.shared',
 'sql_models.shared.file',
 'sql_models.shared.image',
 'sql_models.shared.page',
 'sql_models.shared.role',
 'sql_models.shared.text',
 'sql_models.shared.visibility']

package_data = \
{'': ['*']}

install_requires = \
['camel-model==0.1.0', 'sqlmodel==0.0.6']

setup_kwargs = {
    'name': 'sql-models-infomoto',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'todotom',
    'author_email': 'tomasdarioam@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.10.4',
}


setup(**setup_kwargs)
