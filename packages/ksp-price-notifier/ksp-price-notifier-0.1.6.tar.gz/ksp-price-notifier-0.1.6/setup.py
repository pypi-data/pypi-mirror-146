# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ksp_price_notifier']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ksp-price-notifier = ksp_price_notifier.__main__:app']}

setup_kwargs = {
    'name': 'ksp-price-notifier',
    'version': '0.1.6',
    'description': '',
    'long_description': '# KSP-Price-Notifier\n\nUse to get notified for change of price in KSP.\n\n## Installation\n\n```shell\npip install ksp-price-notifier\n```\n\n## Usage\n\njust give it the uin (can be found the link, as <https://ksp.co.il/web/item/109332>).\ntarget price the the path to chromedriver:\n\n```shell\nksp-price-notifier 109332 5990\n```\n\nresult:\n\n```text\nThe price is lower than the target price, it is now 5549\nGo and buy! https://ksp.co.il/web/item/109332\n```\n\n## In-Code usage\n\n```python\nfrom ksp_price_notifier import GetPriceFromKSP\n\ngetter = GetPriceFromKSP()\ngetter.get_price(109332)\n\n> 4690\n```\n',
    'author': 'Jochman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jochman/KSP-Price-Notifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
