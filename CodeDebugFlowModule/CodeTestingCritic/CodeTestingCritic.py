import logging
from typing import Dict, Any
from aiflows.base_flows import AtomicFlow
from aiflows.interfaces import KeyInterface
from aiflows.messages import FlowMessage

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class CodeTestingCritic(AtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_interface = KeyInterface(keys_to_select=["code", "public_tests_individual_io"])

    def run(self, input_message: FlowMessage):
        input_data = self.input_interface(input_message.data)

        code = input_data["code"]
        test_cases = input_data["public_tests_individual_io"]
        all_tests_passed = True
        testing_results_summary = []

        for test in test_cases:
            try:
                exec_globals = {}
                exec(code, {}, exec_globals)
                function_name = list(exec_globals.keys())[0]
                function = exec_globals[function_name]
                result = function(*test["input"])

                if result == test["expected_output"]:
                    testing_results_summary.append(f"Test passed for input {test['input']}")
                else:
                    testing_results_summary.append(f"Test failed for input {test['input']}: expected {test['expected_output']}, got {result}")
                    all_tests_passed = False
            except Exception as e:
                testing_results_summary.append(f"Test execution error for input {test['input']}: {str(e)}")
                all_tests_passed = False

        reply_message = self.package_output_message(
            input_message,
            response={
                "testing_results_summary": "\n".join(testing_results_summary),
                "all_tests_passed": all_tests_passed
            }
        )
        self.send_message(reply_message)