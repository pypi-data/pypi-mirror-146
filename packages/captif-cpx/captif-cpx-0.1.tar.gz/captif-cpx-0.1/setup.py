# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captif_cpx']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3,<0.11.0',
 'black>=22.3.0,<23.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pyramm>=1.13,<2.0',
 'pyrsona>=0.4,<0.5']

setup_kwargs = {
    'name': 'captif-cpx',
    'version': '0.1',
    'description': '',
    'long_description': '# captif-cpx\n\n\n## Development\n\n### Pre-commit hooks\n\nInstall pre-commit hooks `pre-commit install`.\n\nThe pre-commit hooks will run before each commit. To bypass the pre-commit hooks use `git commit -m \'message\' --no-verify`.\n\n### Testing\n\nRun `./coverage.sh`.\n\n### Publish to PyPI\n\nPushing a tag with format `v*` to the remote repository will trigger a publish to PyPI:\n\n```bash\ngit fetch . dev:master                # merge dev with master\ngit tag -a v0.1 -m "initial release"  # add a version tag\ngit push origin master v0.1           # push master and tag\n```\n\nA Github workflow will automatically run the tests and publish to PyPI if all tests pass.\n',
    'author': 'John Bull',
    'author_email': 'john.bull@nzta.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johnbullnz/pyrsona',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
