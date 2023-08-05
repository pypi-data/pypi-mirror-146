# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multi_event_bus']

package_data = \
{'': ['*']}

install_requires = \
['aioredis[hiredis]>=2.0.1,<3.0.0',
 'jsonschema',
 'redis>=4.2.2,<5.0.0',
 'types-redis>=4.1.19,<5.0.0']

entry_points = \
{'console_scripts': ['all = scripts.poetry_scripts:run_all',
                     'run_black = scripts.poetry_scripts:run_black',
                     'run_flake8 = scripts.poetry_scripts:run_flake8',
                     'run_mypy = scripts.poetry_scripts:run_mypy',
                     'run_pytest = scripts.poetry_scripts:run_pytest',
                     'test = scripts.poetry_scripts:run_all_tests']}

setup_kwargs = {
    'name': 'multi-event-bus',
    'version': '0.2.0',
    'description': 'event bus implementation in python with sync and async support',
    'long_description': '# event-bus\n[![Run Tests](https://github.com/hvuhsg/event-bus/actions/workflows/test.yml/badge.svg)](https://github.com/hvuhsg/event-bus/actions/workflows/test.yml)  \nEventBus implementation in python\n\n\n### Examples\n#### sync\n\n```python\nfrom multi_event_bus import EventBus\n\neb = EventBus(redis_host="127.0.0.1", redis_port=6379)\n\neb.dispatch("event-name", payload={"num": 1})\n\neb.subscribe_to("event-name", consumer_id="consumer-1", offset=0)\n\nevent, topic = eb.get(consumer_id="consumer-1")  # Blocking\n\nprint(event.payload)  # -> {"num": 1}\n```\n#### async\n\n```python\nfrom multi_event_bus import AsyncEventBus\n\neb = AsyncEventBus(redis_host="127.0.0.1", redis_port=6379)\n\neb.dispatch("event-name", payload={"num": 1})\n\neb.subscribe_to("event-name", consumer_id="consumer-2", offset=0)\n\nevent, topic = await eb.get(consumer_id="consumer-2")\n\nprint(event.payload)  # -> {"num": 1}\n```\n#### register event schema\n\n```python\nfrom multi_event_bus import EventBus\n\neb = EventBus(redis_host="127.0.0.1", redis_port=6379)\n\n# Enforce json schema of event\njson_schema = {\n    "type": "object",\n    "properties": {"num": {"type": "string"}}\n}\neb.register_event_schema("event-name", schema=json_schema)\n\neb.dispatch("event-name", payload={"num": "7854"})\n\neb.subscribe_to("event-name", consumer_id="consumer-3", offset=0)\n\nevent, topic = eb.get(consumer_id="consumer-3")  # Blocking\n\nprint(event.payload)  # -> {"num": "7854"}\n```\n\n### Development\n#### scripts\n```commandline\npoetry run run_pytest\npoetry run run_flake8\npoetry run run_mypy\npoetry run run_black\n```\n#### run tests\n```commandline\npoetry run test\n```\n\n#### run all (test and black)\n```commandline\npoetry run all\n```\n',
    'author': 'yehoyada',
    'author_email': 'hvuhsg5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hvuhsg/event-bus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
