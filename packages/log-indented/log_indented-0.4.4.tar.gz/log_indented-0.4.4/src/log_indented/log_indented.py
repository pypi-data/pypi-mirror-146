"""
Basic logging module.
"""
from typing import Any, Callable, cast, TypeVar, Literal, Optional, Tuple, Type
import time
from functools import wraps
import logging
import threading
from types import TracebackType

default_logger: logging.Logger = logging.getLogger(__name__)

PREFIX_ENTER: str = "+ "
PREFIX_EXIT: str = "- "
PREFIX_MESSAGE: str = "  "


class Indentations:
    def __init__(self) -> None:
        self.indents: dict[int, list[Tuple[logging.Logger, str]]] = {}
        self.lock: threading.Lock = threading.Lock()

    def push_logger(self, logger: logging.Logger, name: str) -> None:
        thread_id: int = threading.get_ident()
        with self.lock:
            if thread_id not in self.indents:
                self.indents[thread_id] = []
            self.indents[thread_id].append((logger, name))

    def pop_logger(self) -> None:
        thread_id: int = threading.get_ident()
        with self.lock:
            if thread_id not in self.indents:
                # This points to a likely bug in this class. Log the error, but don't disrupt business logic.
                default_logger.warning("trying to unindent on an untracked thread, %s", thread_id)
                return

            self.indents[thread_id].pop()

            # If we are no longer tracking indentations on this thread, stop tracking, to avoid unnecessarily growing the dictionary.
            if not self.indents[thread_id]:
                del self.indents[thread_id]

    def get_indent_and_logger(self) -> Tuple[int, logging.Logger, str]:
        thread_id: int = threading.get_ident()
        with self.lock:
            if thread_id not in self.indents:
                return 0, default_logger, ""
            logger_to_use, name = self.indents[thread_id][-1]
            indent: int = len(self.indents[thread_id]) - 1
            return indent, logger_to_use, name


class IndentedLog:

    indentations: Indentations = Indentations()

    @staticmethod
    def prepare_compose_log(with_prefix: bool, *args: Any) -> Tuple[str, logging.Logger]:
        indent_level, logger_to_user, name = IndentedLog.indentations.get_indent_and_logger()

        string_to_log: str = PREFIX_MESSAGE if with_prefix else ""
        string_to_log += "  " * (indent_level * 2)
        if with_prefix:
            string_to_log += name + ": "
        for argument in args:
            string_to_log += f"{argument}"

        return string_to_log, logger_to_user

    @staticmethod
    def push_logger(slogger: logging.Logger, name: str) -> None:
        IndentedLog.indentations.push_logger(slogger, name)

    @staticmethod
    def pop_logger() -> None:
        IndentedLog.indentations.pop_logger()

    @staticmethod
    def info(with_prefix: bool, *args: Any) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.info(log_string)

    @staticmethod
    def warning(with_prefix: bool, *args: Any) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.warning(log_string)

    @staticmethod
    def error(with_prefix: bool, *args: Any) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.error(log_string)


def log_info(*args: Any) -> None:
    IndentedLog.info(True, *args)


def log_warn(*args: Any) -> None:
    IndentedLog.warning(True, *args)


def log_error(*args: Any) -> None:
    IndentedLog.error(True, *args)


class LoggedBlock:
    def __init__(self, name: str, flogger: logging.Logger = default_logger) -> None:
        self.start_time: float = 0
        self.name: str = name
        self.logger: logging.Logger = flogger

    def __enter__(self):  # type: ignore
        IndentedLog.push_logger(self.logger, self.name)
        IndentedLog.info(False, f"{PREFIX_ENTER}{self.name}: enter.")
        self.start_time = time.time()
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> Literal[False]:
        duration: float = self.since_start() * 1000.0
        exception_text: str = f"exception: '{exc_type}' - '{exc_value}'" if exc_value else ""
        message_str: str = f"{PREFIX_EXIT}{self.name}: exit. took {duration:,.2f} ms. {exception_text}"
        if exc_value:
            IndentedLog.info(False, message_str)
        else:
            IndentedLog.info(False, message_str)
        IndentedLog.pop_logger()
        return False

    def since_start(self) -> float:
        return time.time() - self.start_time


# pylint: disable=invalid-name
F = TypeVar("F", bound=Callable[..., Any])


def logged(flogger: logging.Logger = default_logger) -> Callable[[F], F]:
    def decorate(function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Logs the timing for a function."""
            with LoggedBlock(function.__qualname__, flogger):
                ret = function(*args, **kwargs)
            return ret

        return cast(F, wrapper)

    return decorate
