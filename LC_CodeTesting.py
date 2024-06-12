from typing import Any, Dict

from aiflows.utils import logging
from .src.evaluation import testing_utils_leetcode
from .CodeTesting import CodeTesting

log = logging.get_logger(__name__)


class LC_CodeTesting(CodeTesting):
    REQUIRED_KEYS_CONFIG = []
    REQUIRED_KEYS_KWARGS = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_test_data(self, input_data: Dict):
        """This function retrieves (or generates) input-output pairs that will be used to test the implementation."""
        return input_data["public_tests_individual_io"]

    def _run_tests(self, input_data: Dict, test_data: Dict) -> Dict[str, Any]:
        testing_results = testing_utils_leetcode.evaluate_solution_for_problem(
            candidate_solution=input_data["code"],
            python_stub=input_data["python_stub"],
            public_tests_io=test_data
        )

        for test_output in testing_results["public_tests_results"]:
            test_output["input"] = "\n".join(test_output["input"])

        return testing_results
