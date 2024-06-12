from typing import Any, Dict

from aiflows import logging
from aiflows.utils.general_helpers import validate_flow_config
from .src.evaluation import testing_utils_codeforces
from .CodeTesting import CodeTesting

log = logging.get_logger(__name__)


class CF_CodeTesting(CodeTesting):
    REQUIRED_KEYS_CONFIG = []
    REQUIRED_KEYS_CONSTRUCTOR = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def _validate_flow_config(cls, kwargs):
        validate_flow_config(cls, kwargs)

        if "public_tests_key" not in kwargs and "hidden_tests_key" not in kwargs:
            raise ValueError("At least one of 'public_tests_key' "
                             "and 'hidden_tests_key' must be specified in the config.")

    def _get_test_data(self, input_data: Dict):
        """This function retrieves (or generates) input-output pairs that will be used to test the implementation."""
        test_data = {"public_tests_io": None, "hidden_tests_io": None}

        if "public_tests_key" in self.flow_config:
            test_data["public_tests_io"] = input_data[self.flow_config["public_tests_key"]]

        if "hidden_tests_key" in self.flow_config:
            test_data["hidden_tests_io"] = input_data[self.flow_config["hidden_tests_key"]]

        return test_data

    def _run_tests(self, input_data: Dict, test_data: Dict) -> Dict[str, Any]:
        testing_results = testing_utils_codeforces.evaluate_solution_for_problem(
            candidate_solution=input_data["code"],
            **test_data
        )

        if "public_tests_results" in testing_results:
            for test_output in testing_results["public_tests_results"]:
                test_output["input"] = "\n".join(test_output["input"])

        if "hidden_tests_results" in testing_results:
            for test_output in testing_results["hidden_tests_results"]:
                test_output["input"] = "\n".join(test_output["input"])

        return testing_results
