# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['materia', 'materia.structure']

package_data = \
{'': ['*']}

install_requires = \
['PubChemPy>=1.0.4,<2.0.0',
 'materia-utils>=1.0.0,<2.0.0',
 'numpy>=1.21.1,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'unyt>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'materia-structure',
    'version': '1.1.0',
    'description': 'Streamlined interface for managing atomistic structure data.',
    'long_description': '========================\nMateria Structure Module\n========================\n\n.. begin-description\n\n.. image:: https://codecov.io/gh/kijanac/materia-structure/branch/main/graph/badge.svg?token=ESFSS6DIMR\n    :target: https://codecov.io/gh/kijanac/materia-structure\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github\n\n**Streamlined interface for managing atomistic structure data.**\n\nStreamlined interface for managing atomistic structure data through Materia. Defines unified and intuitive functionality for manipulating atomistic structure data leveraging the power of Openbabel.\n\n.. end-description\n\n---------------\nGetting Started\n---------------\n\nInstalling\n----------\n.. begin-installing\n\nFrom `pip <https://pypi.org/project/materia-structure/>`_:\n\n``pip install materia-structure``\n\nFrom `conda <https://anaconda.org/kijana/materia-structure>`_:\n\n``conda install -c conda-forge -c kijana materia-structure``\n\n.. end-installing\n\nDocumentation\n-------------\nSee documentation `here <https://kijanac.github.io/materia-structure/>`_.\n\nExamples\n--------\nSee example scripts in `Examples <https://github.com/kijanac/materia-structure/tree/main/examples>`_.\n\n.. begin-about\n\n-------\nAuthors\n-------\nKi-Jana Carter\n\n-------\nLicense\n-------\nThis project is licensed under the MIT License - see the `LICENSE <https://github.com/kijanac/materia-structure/blob/main/LICENSE>`_ file for details.\n\n.. end-about\n\n.. begin-contributing\n\n------------\nContributing\n------------\nSee `CONTRIBUTING <https://github.com/kijanac/materia-structure/blob/main/CONTRIBUTING.rst>`_.\n\n.. end-contributing\n',
    'author': 'Ki-Jana Carter',
    'author_email': 'kijana@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kijanac/materia-structure',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
