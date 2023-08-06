# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['einsum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'einsum',
    'version': '0.2.3',
    'description': 'Experimental implementation of torch/onnx einsum',
    'long_description': "# einsum\n> Experimental implementation of torch/onnx einsum\n\n## Install\n\n```bash\npip3 install -U einsum\n```\n\nOr develop locally:\n```bash\ngit clone https://github.com/sorenlassen/einsum-experiment ~/einsum\ncd ~/einsum\npython3 setup.py develop\n```\n\n## Usage\n\n```py\nimport einsum\n\nprint('TODO')\n```\n\n## Tests\n\nRun `einsum`'s test suite:\n```bash\npip3 install pytest\npytest\n```\n\nType check with mypy:\n```bash\npip3 install mypy\npython3 -m mypy src/einsum/lib.py\n```\n\n## Release\n\nTo publish a new release to pypi:\n```bash\npip3 install python-semantic-release\n\n# verify tests pass.\npytest\n\n# bump the version number, add a git tag.\nsemantic-release version --patch # or --minor, or --major\n\n# push the new version number and tag to github.\ngit push && git push --tags\n\n# publish to pypi.\npoetry build\npoetry publish\n```\n\n## About\n`pyproject.toml` was generated with [mkpylib](https://github.com/shawwn/scrap/blob/master/mkpylib).\n`setup.py` was generated with [poetry-gen-setup-py](https://github.com/shawwn/scrap/blob/master/poetry-gen-setup-py).\n\n",
    'author': 'Soren Lassen',
    'author_email': 'sorenlassen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sorenlassen/einsum-experiment',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
