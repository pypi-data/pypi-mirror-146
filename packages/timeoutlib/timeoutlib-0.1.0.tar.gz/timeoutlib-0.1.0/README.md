# Python Timeout Library

This is the source for the [timeoutlib](https://pypi.org/project/timeoutlib/) python library.

The library solves the following problem: given a computational budget in seconds, and a function that performs some
work, ensure that the computation does not take longer than the budgeted duration

In the event that a function times out, you can choose to return a default value, raise an exception or return a default
from a `default_factory`.

## Usage

You can use a decorator or functional syntax to wrap your function

```python
import time

import timeoutlib


# Decorator syntax

# will raise timeoutlib.OperationTimedOut if 5s exceeded
@timeoutlib.timeout(max_duration=5)
def worker(simulated_duration):
    time.sleep(simulated_duration)


# will return False if 5s exceeded
@timeoutlib.timeout(max_duration=5, default=False)
def worker_default_value(simulated_duration):
    time.sleep(simulated_duration)
    return True


# will call list() to return a new empty list as a default value if 5s exceeded 
@timeoutlib.timeout(max_duration=5, default_factory=list)
def worker_default_value(simulated_duration):
    time.sleep(simulated_duration)
    return True


# will raise a RuntimeError if 5s exceeded 
@timeoutlib.timeout(max_duration=5, exception=RuntimeError)
def worker_default_value(simulated_duration):
    time.sleep(simulated_duration)
    return True


# The two alternative syntax below are equal


@timeoutlib.timeout(max_duration=2)
def worker_decorator(simulated_duration):
    time.sleep(simulated_duration)
    return True


# Given some function that you want to decorate dynamically
def worker_functional(simulated_duration):
    time.sleep(simulated_duration)
    return True


worker_functional = timeoutlib.timeout(max_duration=2)(worker_functional)

# worker_functional and worker_decorated behave the same
```

## Caveats / Notes

- Only supports integer durations (no fractional seconds)
- Uses SIGALRM under the hood (unix only - will not work on Windows)
- `timeoutlib.OperationTimedOut` subclasses the builtin TimeoutError
- The default_factory assumes a function with zero args that returns a new default value
- Accuracy of the timeout duration depends on the underlying OS, Hardware, and some overhead from the decorator itself.