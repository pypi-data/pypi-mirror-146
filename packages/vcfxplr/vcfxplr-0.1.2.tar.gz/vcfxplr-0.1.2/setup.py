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
    'version': '0.1.2',
    'description': 'CLI tool to explore and export data from a VCF / vCard file',
    'long_description': '# vcfxplr\n\n<a href="https://github.com/bergercookie/vcfxplr/actions" alt="CI">\n<img src="https://github.com/bergercookie/vcfxplr/actions/workflows/ci.yml/badge.svg" /></a>\n<a href="https://github.com/pre-commit/pre-commit">\n<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>\n\n<a href="https://github.com/bergercookie/vcfxplr/blob/master/LICENSE.md" alt="LICENSE">\n<img src="https://img.shields.io/github/license/bergercookie/vcfxplr.svg" /></a>\n<a href="https://pypi.org/project/vcfxplr/" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/vcfxplr.svg" /></a>\n<a href="https://badge.fury.io/py/vcfxplr">\n<img src="https://badge.fury.io/py/vcfxplr.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/vcfxplr">\n<img alt="Downloads" src="https://pepy.tech/badge/vcfxplr"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\nThe goal of the tool is to explore and export data from a `VCF` / `vCard` file.\nIt currently serves two functions:\n\n- Reads the `VCF` file and pretty-prints it to stdout\n- Reads the `VCF` file and dumps it in JSON format.\n\n## Installation\n\nInstall it from `PyPI`:\n\n```sh\npip3 install --user --upgrade vcfxplr\n```\n\nTo get the latest version install directly from source:\n\n```sh\npip3 install --user --upgrade git+https://github.com/bergercookie/vcfxplr\n```\n\n## Example - Usage\n\n- Pretty-print a file: `vcfxplr -c path/to/file.vcf pretty`\n- Write to JSON and dump to stdout: `vcfxplr -c path/to/file.vcf json`\n- Write to JSON and dump to stdout - Use `fullname` to group the items: `vcfxplr -c path/to/file.vcf json -g uid`\n\n## Sample Output\n\nSample execution for `vcfxplr -c ~/Downloads/test.vcf json`\n\n```\n2022-04-13 10:30:59.923 | INFO     | vcfxplr.scripts.main:main:87 - Parsing VCF file -> /home/berger/Downloads/test.vcf\n{\n  "John Doe": {\n    "version": [\n      {\n        "value": "4.0"\n      }\n    ],\n    "email": [\n      {\n        "value": "john@doe.com",\n        "params": {\n          "PREF": [\n            "1"\n          ]\n        }\n      },\n      {\n        "value": "john2@doe.com"\n      }\n    ],\n    "n": [\n      {\n        "value": "John  Doe"\n      }\n    ],\n    "tel": [\n      {\n        "value": "+44113712382",\n        "params": {\n          "TYPE": [\n            "home"\n          ],\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      },\n      {\n        "value": "+44113728883",\n        "params": {\n          "TYPE": [\n            "work"\n          ],\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      },\n      {\n        "value": "+44111238885",\n        "params": {\n          "TYPE": [\n            "fax"\n          ],\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      }\n    ],\n    "uid": [\n      {\n        "value": "88cb5e2c-30e3-4b2e-b7bd-ce347a3652a7"\n      }\n    ]\n  },\n  "Ground Control": {\n    "version": [\n      {\n        "value": "4.0"\n      }\n    ],\n    "email": [\n      {\n        "value": "ground@control.com",\n        "params": {\n          "PREF": [\n            "1"\n          ]\n        }\n      }\n    ],\n    "tel": [\n      {\n        "value": "+1123456789",\n        "params": {\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      }\n    ],\n    "uid": [\n      {\n        "value": "7d50ef3d-32be-4b3c-a36b-9a083a8d67b6"\n      }\n    ]\n  },\n  "another  contact": {\n    "version": [\n      {\n        "value": "4.0"\n      }\n    ],\n    "nickname": [\n      {\n        "value": "contact@gmail.com"\n      }\n    ],\n    "n": [\n      {\n        "value": "another   contact"\n      }\n    ],\n    "tel": [\n      {\n        "value": "+12344566789",\n        "params": {\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      }\n    ],\n    "uid": [\n      {\n        "value": "bf2439a6-35cb-4d97-970d-bd31486b61e8"\n      }\n    ]\n  },\n  "one more contact": {\n    "version": [\n      {\n        "value": "4.0"\n      }\n    ],\n    "n": [\n      {\n        "value": "one  more contact"\n      }\n    ],\n    "tel": [\n      {\n        "value": "+49728392882",\n        "params": {\n          "VALUE": [\n            "TEXT"\n          ]\n        }\n      }\n    ],\n    "uid": [\n      {\n        "value": "99b7de2c-26c7-4655-aa19-74c51a1507b0"\n      }\n    ]\n  }\n}\n```\n',
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
