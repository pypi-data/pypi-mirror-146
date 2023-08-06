# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discern', 'discern._scripts', 'discern.estimators', 'discern.mmd']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.16,<0.30.0',
 'click>=7.1.2,<8.0.0',
 'hyperopt>=0.2.3,<0.3.0',
 'joblib>=1.0.1,<2.0.0',
 'llvmlite<0.35.0',
 'ray[tune,default]>=1.6.0,<1.7.0',
 'scanpy>=1.6.0,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'tensorflow-addons>=0.7.1,<0.8.0',
 'tensorflow==2.1.0']

extras_require = \
{'doc': ['Sphinx>=4.1.1,<5.0.0',
         'sphinx-rtd-theme>=0.5.2,<0.6.0',
         'toml>=0.10.2,<0.11.0'],
 'jupyter': ['ipykernel>=5.5.0,<6.0.0']}

entry_points = \
{'console_scripts': ['discern = discern.__main__:main',
                     'merge_parameter = '
                     'discern._scripts.merge_parameters:main']}

setup_kwargs = {
    'name': 'discern-reconstruction',
    'version': '0.1.1',
    'description': 'Wasserstein Auto-Encoder for expression reconstruction',
    'long_description': '\n\n.. image:: https://github.com/imsb-uke/discern/actions/workflows/test.yml/badge.svg\n   :target: https://github.com/imsb-uke/discern/actions/workflows/test.yml\n   :alt: pipeline status\n\n.. image:: https://readthedocs.org/projects/discern/badge/?version=latest\n   :target: https://discern.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/imsb-uke/discern/actions/workflows/dockerimage.yml/badge.svg\n   :target: https://github.com/imsb-uke/discern/actions/workflows/dockerimage.yml\n   :alt: Docker build status\n\nDISCERN\n=======\n\nDISCERN is a deep learning approach to reconstruction expression information\nof single-cell RNAseq data sets using a high quality reference.\n\nGetting Started\n---------------\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\nAn interactive tutorial can be found in `Tutorial.ipynb <https://github.com/imsb-uke/discern/blob/main/Tutorial.ipynb>`_.\n\n\nPrerequisites\n^^^^^^^^^^^^^\n\nWe use `poetry <https://python-poetry.org/>`_ for dependency management. You can get poetry by\n\n.. code-block:: sh\n\n   pip install poetry\n\nor (the officially recommended way)\n\n.. code-block:: sh\n\n   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nInstalling\n^^^^^^^^^^\n\nTo get discern you can clone the repository by\n\n.. code-block:: sh\n\n   git clone https://github.com/imsb-uke/discern.git\n\npoetry can be used to install all further dependencies in an virtual environment.\n\n.. code-block:: sh\n\n   cd discern\n   poetry install --no-dev\n\nTo finally run discern you can also directly use poetry with\n\n.. code-block:: sh\n\n   poetry run commands\n\nor spawn a new shell in the virtual environment\n\n.. code-block:: sh\n\n   poetry shell\n\nFor further examples the first approach is presented.\n\nUsing discern\n^^^^^^^^^^^^^\n\nYou can use the main function of discern for most use cases. Usually you have to preprocess your data by:\n\n.. code-block:: sh\n\n   poetry run discern process <parameters.json>\n\nAn example parameters.json is provided together with an hyperparameter_search.json for hyperparameter optimization using ray[tune].\nThe training can be done with\n\n.. code-block:: sh\n\n   poetry run discern train <parameters.json>\n\nHyperparameter optimization needs a ray server with can be started with\n\n.. code-block:: sh\n\n   poetry run ray start --head --port 57780 --redis-password=\'password\'\n\nand can started with\n\n.. code-block:: sh\n\n   poetry run discern optimize <parameters.json>\n\nFor projection 2 different modes are available:\nEval mode, which is a more general approach and can save a lot of files:\n\n.. code-block:: sh\n\n   poetry run discern project --all_batches <parameters.json>\n\nOr projection mode which offers a more fine grained controll to which is projected.\n\n.. code-block:: sh\n\n   poetry run discern project --metadata="metadatacolumn:value" --metadata="metadatacolumn:" <parameters.json>\n\nwhich creates to files, one is projected to the average batch calculated by a\n``metadatacolumn`` and a contained ``value``.\nThe second file is projected to the the average for each value in "metadatacolumn"; individually.\n\nDISCERN also supports online training. You can add new batches to your dataset after the usual ``train`` with:\n\n.. code-block:: sh\n\n   poetry run discern onlinetraining --freeze --filename=<new_not_preprocessed_batch[es].h5ad> <parameters.json>\n\nThe data gets automatically preprocessed and added to the dataset. You can run ``project`` afterwards as usual (without the ``--filename`` flag).\n``--freeze`` is important to freeze non-conditional layers in training.\n\nTesting\n^^^^^^^\n\nFor critical parts of the model several tests has been implemented. They can be run with:\n\n.. code-block:: sh\n\n   poetry run pytest --cov=discern --cov-report=term\n\n(Requires the development version of discern).\n\nSome tests are slow and don\'t run by default, but you can run them using:\n\n.. code-block:: sh\n\n   poetry run pytest --runslow --cov=discern --cov-report=term\n\nCoding style\n^^^^^^^^^^^^\n\nTo enforce code style guidlines `pylint <https://www.pylint.org/>`_ and `mypy <http://mypy-lang.org/>`_ are use. Example commands are shown below:\n\n.. code-block:: sh\n\n   poetry run pylint discern ray_hyperpara.py\n   poetry run mypy discern ray_hyperpara.py\n\nFor automatic code formatting `yapf <https://github.com/google/yapf>`_ was used:\n\n.. code-block:: sh\n\n   yapf -i <filename.py>\n\nThese tools are included in the dev-dependencies.\n\nAuthors\n-------\n\n* Can Ergen\n* Pierre Machart\n* Fabian Hausmann\n',
    'author': 'Fabian Hausmann',
    'author_email': 'fabian.hausmann@zmnh.uni-hamburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://discern.readthedocs.io/en/latest/quickinfo.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
