import signal
from contextlib import contextmanager
from types import FrameType
from typing import Any, Callable, Union, Type

NOT_ASSIGNED = object()


@contextmanager
def temporary_signal_handler(
        sig: signal.Signals,
        handler: Union[Callable[[signal.Signals, FrameType], Any], int, signal.Handlers, None]
):
    """This context manager ensures that an overwritten signal handler is restored"""
    previous_handler = signal.signal(sig, handler)
    try:
        yield
    finally:
        ...
        signal.signal(sig, previous_handler)


class OperationTimedOut(TimeoutError): ...


def _raise_timeout_error(signum, frame):
    raise TimeoutError


def timeout(
        max_duration: int,
        default: Any = NOT_ASSIGNED,
        default_factory: Callable = None,
        exception: Union[Type[Exception], Exception, None] = None
):
    """
    Wraps a function with a timeout

    Requires an integer timeout value (floats not supported).

    The default behaviour after timeout will be to raise a TimeoutError. This behaviour can be customized by either
    raising a custom Exception or returning a default value (but not both). Assigning both will raise a ValueError
    before invocation.
    """

    assert max_duration >= 1

    if default is not NOT_ASSIGNED and default_factory is not None:
        raise ValueError("Cannot have both default_factory and default specified")

    has_default_or_default_factory = default is not NOT_ASSIGNED or default_factory is not None

    if exception is not None and has_default_or_default_factory:
        raise ValueError("Cannot have a default return value or factory in combination with an exception to raise")

    if not has_default_or_default_factory and exception is None:
        exception = OperationTimedOut

    def decorator(func):

        def inner(*args, **kwargs):
            with temporary_signal_handler(signal.SIGALRM, _raise_timeout_error):
                signal.alarm(max_duration)

                try:
                    result = func(*args, **kwargs)
                except TimeoutError as exc:
                    if exception:
                        raise exception from exc

                    if default_factory:
                        result = default_factory()
                    else:
                        result = default
                finally:
                    signal.alarm(0)

                return result

        return inner

    return decorator
