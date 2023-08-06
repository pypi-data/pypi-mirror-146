# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcfxplr', 'vcfxplr.scripts']

package_data = \
{'': ['*']}

install_requires = \
['bubop>=0.1.6,<0.2.0', 'vobject>=0.9.6,<0.10.0']

entry_points = \
{'console_scripts': ['vcfxplr = vcfxplr.scripts.main:main']}

setup_kwargs = {
    'name': 'vcfxplr',
    'version': '0.1.1',
    'description': 'CLI tool to explore and export data from a VCF / vCard file',
    'long_description': '# vcfxplr\n\n<a href="https://github.com/bergercookie/vcfxplr/actions" alt="CI">\n<img src="https://github.com/bergercookie/vcfxplr/actions/workflows/ci.yml/badge.svg" /></a>\n<a href="https://github.com/pre-commit/pre-commit">\n<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>\n\n<a href="https://github.com/bergercookie/vcfxplr/blob/master/LICENSE.md" alt="LICENSE">\n<img src="https://img.shields.io/github/license/bergercookie/vcfxplr.svg" /></a>\n<a href="https://pypi.org/project/vcfxplr/" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/vcfxplr.svg" /></a>\n<a href="https://badge.fury.io/py/vcfxplr">\n<img src="https://badge.fury.io/py/vcfxplr.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/vcfxplr">\n<img alt="Downloads" src="https://pepy.tech/badge/vcfxplr"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nThe goal of the tool is to explore and export data from a `VCF` / `vCard` file.\nIt currently serves two functions:\n\n- Reads the `VCF` file and pretty-prints it to stdout\n- Reads the `VCF` file and dumps it in JSON format.\n\n## Installation\n\nInstall it from `PyPI`:\n\n```sh\npip3 install --user --upgrade vcfxplr\n```\n\nTo get the latest version install directly from source:\n\n```sh\npip3 install --user --upgrade git+https://github.com/bergercookie/vcfxplr\n```\n\n## Example - Usage\n\n- Pretty-print a file: `vcfxplr -c path/to/file.vcf pretty`\n- Write to JSON and dump to stdout: `vcfxplr -c path/to/file.vcf json`\n- Write to JSON and dump to stdout - Use `fullname` to group the items: `vcfxplr -c path/to/file.vcf json -g fullname`\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/vcfxplr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
