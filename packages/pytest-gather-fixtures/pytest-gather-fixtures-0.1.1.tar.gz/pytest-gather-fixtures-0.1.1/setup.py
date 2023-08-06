# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_gather_fixtures']

package_data = \
{'': ['*']}

install_requires = \
['pytest-asyncio>=0.18.1', 'pytest>=6.0.0']

setup_kwargs = {
    'name': 'pytest-gather-fixtures',
    'version': '0.1.1',
    'description': 'set up asynchronous pytest fixtures concurrently',
    'long_description': "# Pytest-Gather-Fixtures:  run async fixtures concurrently\n\npytest-gather-fixtures is a library for pytest that allows you to set up and tear down fixtures in \nparallel. It's useful for when you have multiple independent fixtures that take a long time to set\nup. \n\n```python\nimport asyncio\nfrom pytest_gather_fixtures import ConcurrentFixtureGroup\n\nmy_fixture_group = ConcurrentFixtureGroup('my_fixture_group')\n\n@my_fixture_group.fixture\nasync def my_fixture_1():\n    await asyncio.sleep(1)\n\n@my_fixture_group.fixture\nasync def my_fixture_2():\n    await asyncio.sleep(1)\n\ndef test_foo(my_fixture_1, my_fixture_2):\n    # setup for this test will only take 1 second\n    pass\n```",
    'author': 'Biocatch LTD',
    'author_email': 'serverteam@biocatch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bentheiii/pytest-gather-fixtures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
