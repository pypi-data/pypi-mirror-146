"""Exception logging decorator, class decorator and metaclass generator."""

import datetime
import functools
import logging
import pathlib
import sys
from typing import Any, Callable, TypeVar

if (sys.version_info.major, sys.version_info.minor) < (3, 6):
    raise Exception("Python 3.6+ required for zoneinfo.")
elif sys.version_info.minor < 9:
    import backports.zoneinfo  # type:ignore

    _zoneinfo = backports.zoneinfo
else:
    import zoneinfo  # type:ignore

    _zoneinfo = zoneinfo

from mypy_extensions import KwArg, VarArg

F = TypeVar("F", bound=Callable[[VarArg(Any), KwArg(Any)], Any])


def exception_logger(filepath: str, timezone: str = "Etc/UTC") -> Callable[[F], F]:
    """
    Creates exception logging decorators.

    Args:
        filepath: Path for created decorator to log exception. Deletes old log file
        if needed.
        timezone: A tz database timezone name.

    Returns:
        Decorator that logs info of an exception which occurs in a function then
        re-raise the exception.
    """
    _filepath = pathlib.Path(filepath).absolute()
    try:
        _filepath.unlink()
    except FileNotFoundError:
        pass
    logging.basicConfig(
        filename=str(_filepath), filemode="a", force=True, level=logging.ERROR
    )
    logger = logging.getLogger()

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            timestamp = str(
                datetime.datetime.now().astimezone(_zoneinfo.ZoneInfo(timezone))
            )
            repr_args = tuple(repr(arg) for arg in args)
            repr_kwargs = {repr(key): repr(value) for key, value in kwargs}
            try:
                output = function(*args, **kwargs)
                return output
            except Exception as error:
                logger.exception(
                    f"{function.__qualname__}\n"
                    f"  raised {error.__class__.__name__}: {str(error)}\n"
                    f"    called with args = {repr_args}, kwargs = {repr_kwargs}\n"
                    f"    at {timestamp}\n"
                )
                raise

        return wrapper

    return decorator


def exception_logger_cls(
    filepath: str, timezone: str = "Etc/UTC"
) -> Callable[[type], type]:
    """
    Creates an exception logging decorator that decorates all methods in a class.

    Args:
        filepath: Path for created decorator to log exception. Deletes old log file
        if needed.
        timezone: A tz database timezone name.
    Returns:
        Decorator that logs info of an exception which occurs in a method then
        re-raise the exception.
    """
    log = exception_logger(filepath, timezone)

    def decorator(cls: type) -> type:
        for key, value in vars(cls).items():
            if isinstance(value, (classmethod, staticmethod)):
                setattr(cls, key, type(value)(log(value.__func__)))
                continue
            elif callable(value):
                setattr(cls, key, log(value))
                continue
        return cls

    return decorator


def exception_logger_meta(filepath: str, timezone: str = "Etc/UTC") -> type:
    """
    Creates an exception logging metaclass that decorates all methods in a class hierarchy.

    Args:
        filepath: Path for created decorator to log exception. Deletes old log file
        if needed.
        timezone: A tz database timezone name.

    Returns:
        Metaclass that logs info of an exception which occurs in a method then
        re-raise the exception.
    """

    class metaclass_(type):
        def __new__(cls, clsname, bases, clsdict):
            return exception_logger_cls(filepath, timezone)(
                super().__new__(cls, clsname, bases, clsdict)
            )

    return metaclass_
