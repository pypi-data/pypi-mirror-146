# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lung-annotator', 'lung-annotator.core', 'lung-annotator.utils']

package_data = \
{'': ['*'], 'lung-annotator': ['scripts/*']}

modules = \
['train', 'predict', 'show', 'model', 'dataset', 'show3d', 'transform']
install_requires = \
['datasets==1.6.2',
 'matplotlib',
 'numpy==1.22.3',
 'pytorch-lightning==1.2.10',
 'scikit-learn==0.24.2',
 'scipy==1.6.1',
 'tensorboard-data-server==0.6.1',
 'tensorboard-plugin-wit==1.8.1',
 'tensorboard==2.8.0',
 'torch==1.9.0',
 'torchaudio==0.9.0',
 'torchmetrics==0.2.0',
 'torchvision==0.12.0',
 'tqdm==4.49.0']

setup_kwargs = {
    'name': 'lung-annotator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mahyar Osanlouy',
    'author_email': 'm.osanlouy@auckland.ac.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
