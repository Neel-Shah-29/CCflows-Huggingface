from typing import Dict, Any

import jinja2

from aiflows.data_transformations.abstract import DataTransformation
from aiflows.utils.general_helpers import unflatten_dict


class TestingResultsSummaryGeneration(DataTransformation):
    def __init__(self, output_key, **kwargs):
        super().__init__(output_key)
        self.params = kwargs
        if "test_results_key" not in self.params:
            self.params["test_results_key"] = "public_tests_results"
        if "tests_passed_key" not in self.params:
            self.params["tests_passed_key"] = "all_tests_passed"

    def __call__(self, data_dict: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if data_dict[self.params["tests_passed_key"]]:
            # the execution did not result in any errors
            data_dict[self.output_key] = self.params["no_error_template"]
            return data_dict

        test_data = unflatten_dict(data_dict)

        if not test_data["compilation_status"]:
            # compilation error occurred
            kwargs = {
                "error_message": test_data["compilation_error_message"].strip(),
            }

            message_content = (
                jinja2.Environment(loader=jinja2.BaseLoader())
                .from_string(self.params["compilation_error_template"])
                .render(**kwargs)
            )
        elif test_data["timeout_error"]:
            # timeout error occurred

            message_content = self.params["timeout_error_template"]
        else:
            # code compiled successfully without timeouts

            # retrieve the failed tests
            failed_tests = [
                test_result
                for test_result in test_data[self.params["test_results_key"]]
                if not test_result["status"]
            ]

            runtime_error_test = None
            for test_result in failed_tests:
                if test_result["generated_output"] is None:
                    # runtime error occurred
                    runtime_error_test = test_result

            if runtime_error_test:
                # construct the error message for the runtime error
                kwargs = {
                    "test_input": runtime_error_test["input"],
                    "error_message": runtime_error_test["error_message"].strip(),
                }

                message_content = (
                    jinja2.Environment(loader=jinja2.BaseLoader())
                    .from_string(self.params["runtime_error_template"])
                    .render(**kwargs)
                )
            else:
                # construct the error message corresponding to a logical error

                if self.params["single_test_error_message"]:
                    # construct the error message for a single (the first) failed test
                    first_failed_test = failed_tests[0]

                    kwargs = {
                        "test_input": first_failed_test["input"],
                        "expected_output": first_failed_test["expected_output"],
                        "generated_output": first_failed_test["generated_output"],
                    }

                    message_content = (
                        jinja2.Environment(loader=jinja2.BaseLoader())
                        .from_string(self.params["single_test_error_template"])
                        .render(**kwargs)
                    )
                else:
                    # construct the error message covering all failed tests
                    parts = [self.params["all_tests_header"]]

                    for idx, test_result in enumerate(failed_tests):
                        kwargs = {
                            "idx": idx + 1,
                            "test_input": test_result["input"],
                            "expected_output": test_result["expected_output"],
                            "generated_output": test_result["generated_output"],
                        }

                        parts.append(
                            jinja2.Environment(loader=jinja2.BaseLoader())
                            .from_string(self.params["test_error_template"])
                            .render(**kwargs)
                        )

                    message_content = self.params["tests_separator"].join(parts)
        data_dict[self.output_key] = message_content
        return data_dict
