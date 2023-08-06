# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todo_cli_typer']

package_data = \
{'': ['*']}

install_requires = \
['colorama==0.4.4', 'shellingham==1.4.0', 'typer==0.3.2']

entry_points = \
{'console_scripts': ['todo = todo_cli_typer.__main__:main']}

setup_kwargs = {
    'name': 'todo-cli-typer',
    'version': '0.3.3',
    'description': 'CLI Todo app with typer and sqlite',
    'long_description': None,
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
