# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['timeoutlib']
setup_kwargs = {
    'name': 'timeoutlib',
    'version': '0.1.0',
    'description': 'Timeout wrapper utilities',
    'long_description': '# Python Timeout Library\n\nThis is the source for the [timeoutlib](https://pypi.org/project/timeoutlib/) python library.\n\nThe library solves the following problem: given a computational budget in seconds, and a function that performs some\nwork, ensure that the computation does not take longer than the budgeted duration\n\nIn the event that a function times out, you can choose to return a default value, raise an exception or return a default\nfrom a `default_factory`.\n\n## Usage\n\nYou can use a decorator or functional syntax to wrap your function\n\n```python\nimport time\n\nimport timeoutlib\n\n\n# Decorator syntax\n\n# will raise timeoutlib.OperationTimedOut if 5s exceeded\n@timeoutlib.timeout(max_duration=5)\ndef worker(simulated_duration):\n    time.sleep(simulated_duration)\n\n\n# will return False if 5s exceeded\n@timeoutlib.timeout(max_duration=5, default=False)\ndef worker_default_value(simulated_duration):\n    time.sleep(simulated_duration)\n    return True\n\n\n# will call list() to return a new empty list as a default value if 5s exceeded \n@timeoutlib.timeout(max_duration=5, default_factory=list)\ndef worker_default_value(simulated_duration):\n    time.sleep(simulated_duration)\n    return True\n\n\n# will raise a RuntimeError if 5s exceeded \n@timeoutlib.timeout(max_duration=5, exception=RuntimeError)\ndef worker_default_value(simulated_duration):\n    time.sleep(simulated_duration)\n    return True\n\n\n# The two alternative syntax below are equal\n\n\n@timeoutlib.timeout(max_duration=2)\ndef worker_decorator(simulated_duration):\n    time.sleep(simulated_duration)\n    return True\n\n\n# Given some function that you want to decorate dynamically\ndef worker_functional(simulated_duration):\n    time.sleep(simulated_duration)\n    return True\n\n\nworker_functional = timeoutlib.timeout(max_duration=2)(worker_functional)\n\n# worker_functional and worker_decorated behave the same\n```\n\n## Caveats / Notes\n\n- Only supports integer durations (no fractional seconds)\n- Uses SIGALRM under the hood (unix only - will not work on Windows)\n- `timeoutlib.OperationTimedOut` subclasses the builtin TimeoutError\n- The default_factory assumes a function with zero args that returns a new default value\n- Accuracy of the timeout duration depends on the underlying OS, Hardware, and some overhead from the decorator itself.',
    'author': 'Imtiaz Mangerah',
    'author_email': 'Imtiaz_Mangerah@a2d24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a2d24/timeoutlib',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
