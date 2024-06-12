from typing import Dict, Any

from aiflows.data_transformations.abstract import DataTransformation


class CorrectnessFlag(DataTransformation):
    def __init__(self, output_key, input_key):
        super().__init__(output_key)
        self.input_key = input_key

    def __call__(self, data_dict: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        all_tests_passed = all([test_result["status"] for test_result in data_dict[self.input_key]])
        data_dict[self.output_key] = all_tests_passed
        return data_dict
