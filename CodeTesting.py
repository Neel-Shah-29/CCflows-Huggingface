from typing import Any, Dict

from aiflows import logging
from aiflows.base_flows import AtomicFlow

log = logging.get_logger(__name__)


class CodeTesting(AtomicFlow):
    REQUIRED_KEYS_CONFIG = []
    REQUIRED_KEYS_CONSTRUCTOR = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_test_data(self, input_data: Dict):
        """This function retrieves (or generates) input-output pairs that will be used to test the implementation."""
        raise NotImplementedError()

    def _run_tests(self, input_data: Dict, test_data: Dict) -> Dict[str, Any]:
        raise NotImplementedError()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # ~~~ Retrieve the test data ~~~
        test_data = self._get_test_data(input_data)

        # ~~~ Run tests ~~~
        response: Dict[str, Any] = self._run_tests(input_data, test_data)

        return response
