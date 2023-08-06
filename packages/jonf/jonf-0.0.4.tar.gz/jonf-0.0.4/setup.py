# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jonf']
setup_kwargs = {
    'name': 'jonf',
    'version': '0.0.4',
    'description': 'JONF parser/formatter in Python',
    'long_description': '# JONF parser/formatter in Python\n\nNOTE: This is an early alpha version\n\n- JONF format docs: https://jonf.app/\n- Formatter is implemented and [tested](https://github.com/whyolet/jonf-py/blob/main/tests/test_format.py)\n- Parser is not implemented [yet](https://jonf.app/#roadmap)\n- Python example:\n\n```python\n# pip install jonf\n\nimport jonf, textwrap\n\ntext = textwrap.dedent(\n    """\\\n    compare =\n      - true\n      = true\n    """\n).rstrip()\n\n# TODO:\n# assert jonf.parse(text) == {"compare": ["true", True]}\n\nassert jonf.format({"compare": ["true", True]}) == text\n```\n',
    'author': 'Denis Ryzhkov',
    'author_email': 'denisr@denisr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whyolet/jonf-py',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
