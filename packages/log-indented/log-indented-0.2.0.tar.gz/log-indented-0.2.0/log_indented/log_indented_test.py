import unittest
import sys
import time

import logging

# pylint: disable=no-name-in-module
from log_indented import logged, log_info, LoggedBlock

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


def f_level_3():
    log_info("level 3: enter")
    f_level_4_with()
    log_info("level 3: exit")


def f_level_4_with():
    with LoggedBlock("with logged block level 4", logger):
        log_info("inside logged block level 4")
        logger.info("just a regular log")


@logged(logger)
def compute_the_answer() -> int:
    for i in range(10):
        time.sleep(0.2)
        log_info(f"{i}, computing the answer")
    return 42


class TestLogIndented(unittest.TestCase):
    @logged(logger)
    def _f_level_2(self):
        log_info("level 2")
        f_level_3()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)

    @logged(logger)
    def _f_level_1(self):
        log_info("level 1")
        self._f_level_2()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)

    @logged(logger)
    def test_basic(self):
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
    def test_important_computation(self):
        with self.assertLogs() as captured:
            the_answer: int = compute_the_answer()
            self.assertEqual(the_answer, 42)

        self._validate_captured_logs(
            expected_lines=[
                "    + compute_the_answer: enter",
                "      compute_the_answer: 0, computing the answer",
                "      compute_the_answer: 1, computing the answer",
                "      compute_the_answer: 2, computing the answer",
                "      compute_the_answer: 3, computing the answer",
                "      compute_the_answer: 4, computing the answer",
                "      compute_the_answer: 5, computing the answer",
                "      compute_the_answer: 6, computing the answer",
                "      compute_the_answer: 7, computing the answer",
                "      compute_the_answer: 8, computing the answer",
                "      compute_the_answer: 9, computing the answer",
                "    - compute_the_answer: exit. took ",
            ],
            captured=captured,
        )

        # self._validate_captured_logs(expected_lines, captured)

    def _validate_captured_logs(self, expected_lines: list[str], captured):
        self.assertEqual(len(captured.records), len(expected_lines))
        for index, expected_string in enumerate(expected_lines):
            self.assertIn(expected_string, captured.records[index].getMessage())

    def setUp(self):
        self.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self.stream_handler)

    def tearDown(self):
        logger.removeHandler(self.stream_handler)
