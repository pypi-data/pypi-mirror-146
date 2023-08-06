# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['config_parser']

package_data = \
{'': ['*']}

extras_require = \
{'yaml': ['PyYAML>=6.0,<7.0']}

setup_kwargs = {
    'name': 'bored-config-parser',
    'version': '0.1.1',
    'description': 'This is a small module you can use to make using config files easy',
    'long_description': '# Bored Config Parser\n\nThis is a small module you can use to make using config files easy\n\n### Example\n\nA config like this:\n```yaml\ngeneral:\n  name: "test"\n  frequency: 22\n\ntargets:\n  - name: "t1"\n    size: "2G"\n  - name: "t2"\n    size: "1G"\n```\n\ncan be easily used with the following code:\n```python\nfrom typing import List\n\nfrom config_parser import load_config\n\n\nclass General:\n    name: str\n    frequency: int\n\n\nclass Target:\n    name: str\n    size: str\n\n    \n@load_config("path/to/config.yaml")\nclass Config:\n    general: General\n    targets: List[Target]\n\n\nprint(Config.general.name)\n\nfor target in Config.targets:\n    print(target.name)\n```\n',
    'author': 'tooboredtocode',
    'author_email': 'bored-coder@tooboredtocode.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tooboredtocode/config-parser',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
