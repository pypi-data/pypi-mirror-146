# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whereval']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'whereval',
    'version': '0.1.2',
    'description': 'Tool for parsing SQL like where expressions and evaluating against live data ',
    'long_description': '## WherEval\n\nTool for parsing SQL like where expressions and evaluating against live data \n\n### Installation\n\n```\npython3 -m pip install whereval\n```\n\n### Inspiration\nThis tool will scratch an itch I\'ve had for some cli tools where I want to pass complex filter expressions to control output / processing.\nFor instance with my `histstat` fork, I would like to have better filtering of networking information to be output to sqlite. See: https://github.com/JavaScriptDude/histstat\n\nAnother usecase for this is a tool I\'ve wanted to write where I can write a `tail -f` wrapper in python where I can define a filter in cli parameters to limit output to the console. Have not written this yet but its on my todo now that I\'ve got this API.\n\n### API Example\n\n#### (Ex1) Basic Concept:\n```python3\nfrom datetime import date\nfrom whereval import Where, util as wutil\n\nprint("\\n(Ex1) Basic Idea")\n\nsw = wutil.StopWatch()\n\n# Where query (terse example)\nqry = "(f0>=2+f1=1+f2=\'s\')|(f3~\'foo%\')"\n\n# Field and type spec\nspec = {\'f0\': int,\'f1\': bool,\'f2\': str,\'f3\': str, \'f4\': dt_date}\n\n# Instantiate Where\n#  - Parses query and uses data to form rules for data types and fields\nwher = Where(query=qry, spec=spec)\n\n\nprint(f"Query:\\n . raw:\\t{qry}\\n . compiled: {wher}\\n\\nTests:")\n\ndef _print(wher, data, tup): \n\t(ok, result, issues) = tup\n\tif not ok:\n\t\tprint(f"Eval failed for {wher}. Issues: {issues}")\n\telse:\n\t\tprint(f"\\t{result}\\tw/ data: {data}")\n\n# Evaluate expression against real data\ndata = {\'f0\': 2, \'f1\': True ,\'f2\': \'s\', \'f3\': \'foobar\'}\n_print(wher, data, wher.evaluate(data))\n\n# For different data\ndata[\'f3\'] = \'bazbar\'\n_print(wher, data, wher.evaluate(data))\n\n# For different data\ndata[\'f0\'] = 1\n_print(wher, data, wher.evaluate(data))\n\nprint(f"Completed. Elapsed: {sw.elapsed(3)}s")\n```\n\n#### Output of print:\n```\n(Ex1) Basic Idea\nQuery:\n . raw:\t(f0>=2+f1=1+f2=\'s\')|(f3~\'foo%\')\n . compiled: ( ( f0 >= 2 AND f1 = 1 AND f2 = \'s\' ) OR ( f3 like \'foo%\' ) )\n\nTests:\n\tTrue\tw/ data: {\'f0\': 2, \'f1\': True, \'f2\': \'s\', \'f3\': \'foobar\'}\n\tTrue\tw/ data: {\'f0\': 2, \'f1\': True, \'f2\': \'s\', \'f3\': \'bazbar\'}\n\tFalse\tw/ data: {\'f0\': 1, \'f1\': True, \'f2\': \'s\', \'f3\': \'bazbar\'}\nCompleted. Elapsed: 0.003s\n```\n\n\n### Query Syntax:\n\n```\n# General:\n#  Query must begin with \'(\' and end with \')\'\n#  NOT, IN, BETWEEN must be followed by parenthesis \'(\'\n# Boolean Operators:\n#   AND, OR, NOT\n# Equality Operators:\n#  =, !=, <, <=, >, >=, like\n# Special:\n#   !   -->  NOT\n#   +   -->  AND\n#   |   -->  OR\n#   <>  -->  !=\n#   ~   -->  like\n```\n\n### TODO:\n* [.] implement `in (v1, v2, v3)` clauses\n* [.] implement `between (v1, v2)` clauses',
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
