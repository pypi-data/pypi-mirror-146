# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yni']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yni',
    'version': '0.0.2',
    'description': 'A parser for the yni config file.',
    'long_description': '# yni\n\nA parser for the yni config file.\n\n## Example\n\ntest.py\n\n```py\nfrom yni import Yni\n\nparser = Yni.from_file(\'example.yni\') # here we parse from a file\n\nparser[\'foo\'][\'bar\'] # get the value of the key "bar" from the header "foo", returns "spam"\n# or\nparser.foo.bar # returns "spam"\n```\n\n## Example 2\n\ntest_2.py\n\n```py\nfrom yni import Yni\n\n string = """#foo\n [\n     bar: spam\n ]"""\n\nparser = Yni.from_string(string) # here we parse from a string\n\nparser[\'foo\'][\'bar\'] # get the value of the key "bar" from the header "foo", returns "spam"\n# or\nparser.foo.bar # returns "spam"\n```\n\n## yni file structure\n\nexample.yni\n\n```yni\n#foo\n[\n    bar: spam\n]\n```\n',
    'author': 'Alex Hutz',
    'author_email': 'frostiiweeb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FrostiiWeeb/yni',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
