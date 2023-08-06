import unittest
from unittest._log import _LoggingWatcher
import sys
import time

import logging

# pylint: disable=no-name-in-module
from log_indented import logged, log_info, log_warn, log_error, LoggedBlock  # type: ignore

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


def f_level_3() -> None:
    log_info("level 3: enter")
    f_level_4_with()
    log_info("level 3: exit")


def f_level_4_with() -> None:
    with LoggedBlock("with logged block level 4", logger):
        log_info("inside logged block level 4")
        logger.info("just a regular log")


@logged(logger)
def count_chicken() -> int:
    return 3


@logged(logger)
def count_ducks() -> int:
    return 7


@logged(logger)
def count_birds() -> int:
    return count_chicken() + count_ducks()


@logged(logger)
def count_goats() -> int:
    return 7


@logged(logger)
def count_sheep() -> int:
    return 0


@logged(logger)
def count_barnyard_animals() -> int:
    total_animal_count: int = count_birds() + count_goats() + count_sheep()
    log_info(f"total barnyard animals: {total_animal_count}")
    return total_animal_count


@logged(logger)
def compute_element() -> int:
    time.sleep(0.1)
    return 3


@logged(logger)
def compute_the_answer() -> int:
    result: int = sum([compute_element() for x in range(10)])
    log_info(f"result: {result}")
    return result


class TestLogIndented(unittest.TestCase):
    @logged(logger)
    def _f_level_2(self) -> None:
        log_info("level 2")
        f_level_3()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)

    @logged(logger)
    def _f_level_1(self) -> None:
        log_info("level 1")
        self._f_level_2()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)

    def test_with_default_logger(self) -> None:
        @logged()
        def somefunction() -> None:
            log_info("testing")

        with self.assertLogs() as captured:
            somefunction()

        self._validate_captured_logs(
            expected_lines=[
                "+ TestLogIndented.test_with_default_logger.<locals>.somefunction: enter",
                "  TestLogIndented.test_with_default_logger.<locals>.somefunction: testing",
                "- TestLogIndented.test_with_default_logger.<locals>.somefunction: exit. took ",
            ],
            captured=captured,
        )

    def test_log_types(self) -> None:
        with self.assertLogs() as captured:
            log_info("info")
            log_warn("warning")
            log_error("error")

        self._validate_captured_logs(
            expected_lines=[
                "info",
                "warning",
                "error",
            ],
            captured=captured,
        )

    def test_exception(self) -> None:
        @logged(logger)
        def raises_exception() -> None:
            raise RuntimeError("something bad happened")

        with self.assertLogs() as captured:
            with self.assertRaises(RuntimeError):
                raises_exception()

        self._validate_captured_logs(
            expected_lines=[
                "+ TestLogIndented.test_exception.<locals>.raises_exception: enter",
                "- TestLogIndented.test_exception.<locals>.raises_exception: exit. "
                "took 0.00 ms. exception: '<class 'RuntimeError'>' - 'something bad happened'",
            ],
            captured=captured,
        )

    def test_not_logged(self) -> None:
        with self.assertLogs() as captured:
            logger.info("chickens!")
            log_info("ducks")

        self._validate_captured_logs(
            expected_lines=[
                "chickens!",
                "ducks",
            ],
            captured=captured,
        )

    @logged(logger)
    def test_basic(self) -> None:
        with self.assertLogs() as captured:
            self._f_level_1()

        self._validate_captured_logs(
            expected_lines=[
                "+ TestLogIndented._f_level_1: enter",
                "  TestLogIndented._f_level_1: level 1",
                "    + TestLogIndented._f_level_2: enter",
                "      TestLogIndented._f_level_2: level 2",
                "      TestLogIndented._f_level_2: level 3: enter",
                "        + with logged block level 4: enter",
                "          with logged block level 4: inside logged block level 4",
                "just a regular log",
                "        - with logged block level 4: exit. took ",
                "      TestLogIndented._f_level_2: level 3: exit",
                "    - TestLogIndented._f_level_2: exit. took ",
                "- TestLogIndented._f_level_1: exit. took ",
            ],
            captured=captured,
        )

    @logged(logger)
    def test_count_animals(self) -> None:
        with self.assertLogs() as captured:
            animal_count: int = count_barnyard_animals()
            self.assertEqual(animal_count, 17)
        self._validate_captured_logs(
            expected_lines=[
                "    + count_barnyard_animals: enter",
                "        + count_birds: enter",
                "            + count_chicken: enter",
                "            - count_chicken: exit. took ",
                "            + count_ducks: enter",
                "            - count_ducks: exit. took ",
                "        - count_birds: exit. took ",
                "        + count_goats: enter",
                "        - count_goats: exit. took ",
                "        + count_sheep: enter",
                "        - count_sheep: exit. took ",
                "      count_barnyard_animals: total barnyard animals: 17",
                "    - count_barnyard_animals: exit. took ",
            ],
            captured=captured,
        )

    @logged(logger)
    def test_important_computation(self) -> None:
        with self.assertLogs() as captured:
            the_answer: int = compute_the_answer()
            self.assertEqual(the_answer, 30)

        self._validate_captured_logs(
            expected_lines=[
                "    + compute_the_answer: enter",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "        + compute_element: enter",
                "        - compute_element: exit. took ",
                "      compute_the_answer: result: 30",
                "    - compute_the_answer: exit. took ",
            ],
            captured=captured,
        )

    def _validate_captured_logs(self, expected_lines: list[str], captured: _LoggingWatcher) -> None:
        self.assertEqual(len(captured.records), len(expected_lines))
        for index, expected_string in enumerate(expected_lines):
            self.assertIn(expected_string, captured.records[index].getMessage())

    def setUp(self) -> None:
        self.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self.stream_handler)

    def tearDown(self) -> None:
        logger.removeHandler(self.stream_handler)
