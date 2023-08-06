# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tetris', 'tetris.engine']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0', 'typing-extensions>=4.0.1,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=4.4.0,<5.0.0',
          'furo>=2022.3.4,<2023.0.0',
          'numpydoc>=1.2,<2.0']}

setup_kwargs = {
    'name': 'tetris',
    'version': '0.6.0',
    'description': 'Simple and modular tetris library',
    'long_description': '# python-tetris: a simple and modular tetris library\n\n[![pypi](https://img.shields.io/pypi/v/tetris?logo=pypi&logoColor=f0f0f0&style=for-the-badge)](https://pypi.org/project/tetris/)\n[![versions](https://img.shields.io/pypi/pyversions/tetris?logo=python&logoColor=f0f0f0&style=for-the-badge)](https://pypi.org/project/tetris/)\n[![build](https://img.shields.io/github/workflow/status/dzshn/python-tetris/Test%20library?logo=github&logoColor=f0f0f0&style=for-the-badge)](https://github.com/dzshn/python-tetris/actions/workflows/test.yml)\n[![technical-debt](https://img.shields.io/badge/contains-technical%20debt-009fef?style=for-the-badge)](https://forthebadge.com/)\n\n---\n\n## Intro\n\nA simple and modular library for implementing and analysing Tetris games, [guideline](https://archive.org/details/2009-tetris-variant-concepts_202201)-compliant by default\n\n```py\n>>> import tetris\n>>> game = tetris.BaseGame(board_size=(4, 4), seed=128)\n>>> game.engine\nEngine(gravity=InfinityGravity, queue=SevenBag, rs=SRS, scorer=GuidelineScorer)\n>>> game.queue\nSevenBag([PieceType.J, PieceType.O, PieceType.L, PieceType.I, PieceType.T, PieceType.S, PieceType.J])\n>>> for _ in range(4): game.hard_drop()\n>>> game.playing\nFalse\n>>> print(game)\nJ O O\nJ J J\nZ Z\n  Z Z\n```\n\n## Links\n\n- [Documentation](https://python-tetris.readthedocs.io/)\n- [PyPI](https://pypi.org/project/tetris)\n- Support: [create an issue](https://github.com/dzshn/python-tetris/issues/new/choose) or [see author contact](https://dzshn.xyz)\n\n## Install\n\nThis package is available on [PyPI](https://pypi.org/project/tetris/), you can install it with pip:\n\n```sh\npip install tetris\n# or `py -m pip ...` etc.\n```\n\nTo install the git version:\n\n```sh\npip install git+https://github.com/dzshn/python-tetris\n```\n',
    'author': 'Sofia "dzshn" N. L.',
    'author_email': 'zshn@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dzshn/python-tetris',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
