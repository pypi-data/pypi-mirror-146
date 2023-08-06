# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teddy_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]<0.4.0']

entry_points = \
{'console_scripts': ['teddy-portal-gun = teddy_portal_gun.main:app']}

setup_kwargs = {
    'name': 'teddy-portal-gun',
    'version': '0.2.0',
    'description': '',
    'long_description': '# `teddy-portal-gun`\n\nAwesome Portal Gun\n\n**Usage**:\n\n```console\n$ teddy-portal-gun [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `load`: Load the portal gun\n* `shoot`: Shoot the portal gun\n\n## `teddy-portal-gun load`\n\nLoad the portal gun\n\n**Usage**:\n\n```console\n$ teddy-portal-gun load [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `teddy-portal-gun shoot`\n\nShoot the portal gun\n\n**Usage**:\n\n```console\n$ teddy-portal-gun shoot [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'Teddy Xinyuan Chen',
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
