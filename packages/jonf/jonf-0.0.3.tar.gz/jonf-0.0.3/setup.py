# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jonf']
setup_kwargs = {
    'name': 'jonf',
    'version': '0.0.3',
    'description': 'JONF parser/formatter in Python',
    'long_description': '# JONF parser/formatter in Python\n\nNOTE: This is initial stub version, docs and tests only\n\n- JONF format: https://jonf.app/\n\n- Python example:\n\n```python\n# pip install jonf\n\nimport jonf\n\ntext = """\\\ncompare =\n  - true\n  = true\n"""\n\nassert jonf.parse(text) == {"compare": ["true", True]}\n\nassert jonf.format({"compare": ["true", True]}) == text\n```\n\n- TODO: Implement `jonf.parse()` and `jonf.format()` as part of [JONF Roadmap](https://jonf.app/#roadmap)\n',
    'author': 'Denis Ryzhkov',
    'author_email': 'denisr@denisr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whyolet/jonf-py',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
