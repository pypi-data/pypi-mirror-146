# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chris', 'chris.cube', 'chris.helpers']

package_data = \
{'': ['*']}

install_requires = \
['pyserde>=0.7.1,<0.8.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'caw',
    'version': '0.7.0a1',
    'description': 'ChRIS client library',
    'long_description': '# Python _ChRIS_ Client\n\n[![PyPI](https://img.shields.io/pypi/v/caw)](https://pypi.org/project/caw/)\n[![License - MIT](https://img.shields.io/pypi/l/caw)](https://github.com/FNNDSC/caw/blob/master/LICENSE)\n[![CI](https://github.com/FNNDSC/caw/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/caw/actions)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python _ChRIS_ client library.\n\n## Installation\n\n```shell\npip install -U caw\n```\n\n## Example\n\n```python\nfrom pathlib import Path\nfrom chris.client import ChrisClient\n\nclient = ChrisClient.from_login(\n    address="https://cube.chrisproject.org/api/v1/",\n    username="chris",\n    password="chris1234"\n)\nclient.upload(Path("example.txt"), "my_examples")\ndircopy = client.get_plugin_by_name("pl-dircopy")\nplinst = dircopy.create_instance({"dir": "chris/uploads/my_examples/example.txt"})\n```\n\n## Async\n\nLooking for an `async` _ChRIS_ client? Let us know!\nWe have one implemented\n[here](https://github.com/FNNDSC/chrisomatic/tree/master/chris),\nthough it\'s not published to PyPI.\n\n## Command-Line Client\n\n[chrs](https://github.com/FNNDSC/chrs/tree/master/chrs#readme)\nis the next-generation _ChRIS_ command-line client, please check it out.\n\n`caw` previously included a command-line client for _ChRIS_, however\nsince v0.7.0 it was deprecated and removed.\n\nTo use the `caw` command:\n\n```shell\npip install caw==0.6.1\n```\n\nUsage: https://github.com/FNNDSC/caw/blob/d5b05b28af312b97ac80bd96376d70626db737a5/README.md\n',
    'author': 'FNNDSC',
    'author_email': 'dev@babyMRI.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chrisproject.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
