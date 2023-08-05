# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kithon']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<4.0.0',
 'PyYaml>=5.4.0',
 'pyxl4>=1.0.0-alpha.1,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['kithon = kithon.cli:tpy',
                     'kithon-gen = kithon.cli:tpy_gen',
                     'kithon-new = kithon.cli:tpy_new']}

setup_kwargs = {
    'name': 'kithon',
    'version': '0.2.1',
    'description': 'transpiler python into other language',
    'long_description': '**Kithon** is a project that provides the ability to translate python and python-family language such as\n[hy-lang](https://github.com/hylang/hy) and [coconut](https://github.com/evhub/coconut)\ninto human-readable code in any other programming languages.\n\n[Try out the web demo](https://alploskov.github.io/kithon/demo/)\n\nor \n\n```bash\npip install kithon\n\necho "print(\'Hello World\')" > test.py\n\nkithon gen --js test.py\n```\n\nOutput:\n\n```js\nconsole.log("Hello World");\n```\n\nFor what?\n---------\n\nFor use python where we can\'t. For example in browser(js), embedded scripting(mostly lua).\nOr make python program faster by translating to go, c++, rust, nim or julia.\nAlso for supporting program written on in unpopular programming languages (very new or vice versa)\n\nHow it works?\n-------------\n\nKithon uses a dsl based on yaml and jinja to apply the rules described on it to the nodes of the ast tree. \nUsing this dsl you can add new languages or extensions to those already added.\n\nStatus\n------\n\nThe project is under active development.\nNow the ability to add translation of basic python constructs into any other language(in this repo js and go only) is supported.\n\nThere are plans to develop a number of supported languages and expand support for python syntax\n\nSimilar projects\n----------------\n\n* [py2many](https://github.com/adsharma/py2many)\n* [pseudo](https://github.com/pseudo-lang/pseudo)',
    'author': 'Aleksey Ploskov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alploskov/kithon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<3.11',
}


setup(**setup_kwargs)
