# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uganda_uber_switching_reg', 'uganda_uber_switching_reg.simulation']

package_data = \
{'': ['*'], 'uganda_uber_switching_reg': ['saved_models/plots/*']}

install_requires = \
['linearmodels==4.24',
 'matplotlib==3.4.3',
 'numpy==1.20.3',
 'pandas==1.3.2',
 'patsy==0.5.2',
 'scikit-learn==0.24.2',
 'scipy==1.7.1',
 'statsmodels==0.12.2',
 'tqdm==4.56.0']

setup_kwargs = {
    'name': 'uganda-uber-switching-reg',
    'version': '0.2.0',
    'description': 'A robust estimator to machine learning prediction misclassification',
    'long_description': None,
    'author': 'Aleksandr Michuda',
    'author_email': 'amichuda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
