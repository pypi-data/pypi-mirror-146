# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gooder']
install_requires = \
['cssselect>=1.1.0,<2.0.0', 'lxml>=4.8.0,<5.0.0', 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'gooder',
    'version': '0.2',
    'description': 'Simple Google parser',
    'long_description': '# <b>GOO</b>gle spi<b>DER</b>\nGoogle search engine parser on python3\n\n## Instruction\n> Requirement python 3.10+\n\n> python3 -m pip install -r requirements.txt\n\n```python\nimport gooder\n\ngooder = Gooder()\n# Make request on google.com/search?q=Hello+World\ngooder.parse(query="Hello World")\n\n# Print only result links\nprint(gooder.get_links())\n\n# Print only result titles\nprint(gooder.get_titles())\n\n# Print all results list[tuple[link,title]]\nprint(gooder.raw_results)\n\n# Save urls to json file\ngooder.save_to_file(only_urls=True, to_json=True, override=True, file="results.json")\n```\n\n## Methods & Fields\n| Method/Field | Args | Example | Result |\n|---|---|---|---|\n| Gooder.parse | query: str, page: int=0, ignore_google: bool=True, clear_old: bool=True | gooder.parse("hello",  clear_old=False) | See below |\n| Gooder.raw_results | **Field** | **Field** | [[link, title], ...] |\n| Gooder.get_links | repeats: bool = False | gooder.get_links() | [unique_link, ...] |\n| Gooder.get_titles | *None* | gooder.get_titles() | [title, title, ...] |\n| Gooder.save_to_file | only_urls: bool = True override: bool = True to_json: bool = False file: str = "urls.txt"  | gooder.save_to_file() | New file with urls |\n| Gooder.get_hostname | links: str \\| list | gooder.get_hostname( https://google.com/) | google.com |\n\n## Todo:\n + Detect captcha\n + Add proxy manager',
    'author': 'slavatar',
    'author_email': 'nslavatar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/9Slavatar/gooder',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
