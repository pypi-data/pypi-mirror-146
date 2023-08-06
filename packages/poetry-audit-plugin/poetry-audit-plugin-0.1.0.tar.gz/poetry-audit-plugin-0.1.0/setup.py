# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_audit_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0b1,<2.0.0', 'safety>1.0.0,<=1.10.3']

entry_points = \
{'poetry.application.plugin': ['poetry-audit-plugin = '
                               'poetry_audit_plugin.plugin:AuditApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-audit-plugin',
    'version': '0.1.0',
    'description': 'Poetry plugin for checking security vulnerabilities in dependencies',
    'long_description': '# Poetry Audit Plugin\n\nPoetry plugin for checking security vulnerabilities in dependencies based on [safety](https://github.com/pyupio/safety).\n\n```\n$ poetry audit\nScanning 19 packages...\n\n  • ansible-runner     installed 1.1.2  affected <1.3.1   CVE PVE-2021-36995\n  • ansible-tower-cli  installed 3.1.8  affected <3.2.0   CVE CVE-2020-1733 \n  • jinja2             installed 2.0    affected <2.11.3  CVE CVE-2020-28493\n\n3 vulnerabilities found\n```\n\n## Installation\n\nThe easiest way to install the `export` plugin is via the `plugin add` command of Poetry.\n\n```bash\npoetry plugin add poetry-audit-plugin\n```\n\nIf you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.\n\n```bash\npipx inject poetry poetry-audit-plugin\n```\n\nOtherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.\n\n```bash\npip install poetry-audit-plugin\n```\n\n## Available options\n\n* `--json`: Export the result in JSON format.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'opeco17',
    'author_email': 'opeco17@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opeco17/poetry-audit-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
