# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diive',
 'diive.configs.filetypes',
 'diive.core',
 'diive.core.dfun',
 'diive.core.io',
 'diive.core.ml',
 'diive.core.plotting',
 'diive.core.plotting.styles',
 'diive.core.utils',
 'diive.pkgs',
 'diive.pkgs.analyses',
 'diive.pkgs.corrections',
 'diive.pkgs.createflag',
 'diive.pkgs.createvar',
 'diive.pkgs.echires',
 'diive.pkgs.flux',
 'diive.pkgs.gapfilling',
 'diive.pkgs.outlierdetection',
 'diive.pkgs.qaqc']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Sphinx>=4.3.2,<5.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pysolar>=0.10,<0.11',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'statsmodels>=0.13.1,<0.14.0',
 'uncertainties>=3.1.6,<4.0.0']

setup_kwargs = {
    'name': 'diive',
    'version': '0.31.0',
    'description': 'Time series post-processing and analysis',
    'long_description': None,
    'author': 'Lukas Hörtnagl',
    'author_email': 'holukas@ethz.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
