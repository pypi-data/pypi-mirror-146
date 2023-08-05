# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whereval']

package_data = \
{'': ['*'], 'whereval': ['.vscode/*']}

setup_kwargs = {
    'name': 'whereval',
    'version': '0.0.1',
    'description': 'Tool for parsing SQL like where expressions and evaluating against live data ',
    'long_description': '## WherEval\n\nTool for parsing SQL like where expressions and evaluating against live data \n\n### Installation\n\n```\npython3 -m pip install whereval\n```\n\n### API Example\n\n#### (Ex1) Basic Concept:\n```python3\nfrom datetime import date\nfrom whereval import Where, util as wutil\n\nprint("\\n(Ex1) Basic Idea")\n\nsw = wutil.StopWatch()\n\n# Where query (terse example)\nqry = "(f0>=2+f1=1+f2=\'s\')|(f3~\'foo%\')"\n\n# Template for defining data types and fields allowed in query\nd_tmpl = {\'f0\': 0,\'f1\': True,\'f2\': \'s\',\'f3\': \'s\', \'f4\': date(1970,1,1)}\n\n# Instantiate Where\n#  - Parses query and uses data to form rules for data types and fields\nwher = Where(query=qry, data_tmpl=d_tmpl)\n\n\nprint(f"Query:\\n . raw:\\t{qry}\\n . compiled: {wher}\\n\\nTests:")\n\ndef _print(w, d, b): print(f"\\t{b}\\tw/ data: {d}")\n\n# Evaluate expression against real data\ndct = {\'f0\': 2, \'f1\': True ,\'f2\': \'s\', \'f3\': \'foobar\'}\n_print(wher, dct, wher.evaluate(dct))\n\n# For different data\ndct[\'f3\'] = \'bazbar\'\n_print(wher, dct, wher.evaluate(dct))\n\n# For different data\ndct[\'f0\'] = 1\n_print(wher, dct, wher.evaluate(dct))\n\nprint(f"Completed. Elapsed: {sw.elapsed(3)}s")\n```\n\nOutput of print:\n```\n(Ex1) Basic Idea\nQuery:\n . raw:\t(f0>=2+f1=1+f2=\'s\')|(f3~\'foo%\')\n . compiled: ( ( f0 >= 2 AND f1 = 1 AND f2 = \'s\' ) OR ( f3 like \'foo%\' ) )\n\nTests:\n\tTrue\tw/ data: {\'f0\': 2, \'f1\': True, \'f2\': \'s\', \'f3\': \'foobar\'}\n\tTrue\tw/ data: {\'f0\': 2, \'f1\': True, \'f2\': \'s\', \'f3\': \'bazbar\'}\n\tFalse\tw/ data: {\'f0\': 1, \'f1\': True, \'f2\': \'s\', \'f3\': \'bazbar\'}\nCompleted. Elapsed: 0.003s\n```\n\n\n### Query Syntax:\n\n```\n# Conditions:\n#   AND / OR\n# Special Conditions:\n#   + --> AND\n#   | --> OR\n# Operators:\n#  =, !=, <, <=, >, >=, like\n# Special Operators:\n#   <> --> !=\n#    ~ --> like\n```',
    'author': 'Timothy C. Quinn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/whereval',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
