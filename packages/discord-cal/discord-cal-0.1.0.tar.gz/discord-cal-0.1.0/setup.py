# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discal']

package_data = \
{'': ['*']}

install_requires = \
['ics>=0.7,<0.8', 'pypresence>=4.2.1,<5.0.0', 'pytz>=2022.1,<2023.0']

entry_points = \
{'console_scripts': ['discord-cal = discal:__main__.main']}

setup_kwargs = {
    'name': 'discord-cal',
    'version': '0.1.0',
    'description': '',
    'long_description': '# discord-cal\n\nPublish your status on discord using data from an iCal calendar over a rich presence.\n\n## Installation and usage\n\n```bash\npip install discord-cal\n```\n\n```bash\ndiscord-cal -i <app_id> -c <calendar_id>\n```\n\nIf you would like details, include the `-d` flag.\n',
    'author': 'Parker Wahle',
    'author_email': 'parkeredwardwahle2017@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/regulad/discord-cal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
