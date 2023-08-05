"""
Basic logging module.
"""
from typing import Tuple
import time
from functools import wraps
import logging
import threading

default_logger: logging.Logger = logging.getLogger(__name__)

PREFIX_ENTER: str = "+ "
PREFIX_EXIT: str = "- "
PREFIX_MESSAGE: str = "  "


class Indentations:
    def __init__(self):
        self.indents: dict[int, list] = {}
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
    def prepare_compose_log(with_prefix: bool, *args) -> Tuple[str, logging.Logger]:
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
    def info(with_prefix: bool, *args) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.info(log_string)

    @staticmethod
    def warning(with_prefix: bool, *args) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.warning(log_string)

    @staticmethod
    def error(with_prefix: bool, *args) -> None:
        log_string, logger_to_use = IndentedLog.prepare_compose_log(with_prefix, *args)
        logger_to_use.error(log_string)


def log_info(*args) -> None:
    IndentedLog.info(True, *args)


def log_warn(*args) -> None:
    IndentedLog.warning(True, *args)


def log_error(*args) -> None:
    IndentedLog.error(True, *args)


class LoggedBlock:
    def __init__(self, name, flogger=default_logger):
        self.start_time: float = 0
        self.name: str = name
        self.logger = flogger

    def __enter__(self):
        IndentedLog.indentations.push_logger(self.logger, self.name)
        IndentedLog.info(False, f"{PREFIX_ENTER}{self.name}: enter")
        # self.logger.info(self.name + ": enter")
        self.start_time = int(time.time())
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        duration: float = self.since_start() * 1000.0
        exception_text: str = f"exception: '{exc_type}' - '{exc_value}'" if exc_value else ""
        message_str: str = f"{PREFIX_EXIT}{self.name}: exit. took {duration:,.1f} ms. {exception_text}"
        if exc_value:
            IndentedLog.info(False, message_str)
        else:
            IndentedLog.info(False, message_str)
        IndentedLog.indentations.pop_logger()

    def since_start(self) -> float:
        return time.time() - self.start_time


def logged(flogger=default_logger):
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Logs the timing for a function."""
            with LoggedBlock(function.__qualname__, flogger):
                ret = function(*args, **kwargs)
            return ret

        return wrapper

    return decorate
