import os

from aiflows import logging
from aiflows.utils.general_helpers import read_yaml_file
from aiflows.flow_cache import CACHING_PARAMETERS, clear_cache
from aiflows.utils import serving
from aiflows.utils.colink_utils import start_colink_server
from aiflows.workers import run_dispatch_worker_thread

CACHING_PARAMETERS.do_caching = False  # Set to True to enable caching

logging.set_verbosity_debug()

dependencies = [
    {"url": "aiflows/CodeTestingCriticFlowModule", "revision": os.getcwd()},
]

from aiflows import flow_verse
flow_verse.sync_dependencies(dependencies)

if __name__ == "__main__":

    FLOW_MODULES_PATH = "./"
    # Set up a colink server
    cl = start_colink_server()

    # Load flow config
    root_dir = "."
    cfg_path = os.path.join(root_dir, "CodeTestingCritic.yaml")
    cfg = read_yaml_file(cfg_path)

    # Serve the Flow
    serving.recursive_serve_flow(
        cl=cl,
        flow_class_name="flow_modules.aiflows.CodeTestingCriticFlowModule.CodeTestingCritic",
        flow_endpoint="CodeTestingCritic",
    )

    # Start a Worker Thread
    run_dispatch_worker_thread(cl)

    # Mount the flow and get its proxy
    proxy_flow = serving.get_flow_instance(
        cl=cl,
        flow_endpoint="CodeTestingCritic",
        user_id="local",
        config_overrides=cfg
    )

    # Prepare data
    data = {
        "id": 0,
        "code": "def add(a, b): return a + b",
        "public_tests_individual_io": [
            {"input": [1, 2], "expected_output": 3},
            {"input": [-1, 5], "expected_output": 4},
            {"input": [10, -20], "expected_output": -10}
        ]
    }

    input_message = proxy_flow.package_input_message(data=data)

    # Run inference
    future = proxy_flow.get_reply_future(input_message)
    reply_data = future.get_data()

    # Print the output
    print("~~~~~~Reply from CodeTestingCriticFlow~~~~~~")
    print(reply_data)