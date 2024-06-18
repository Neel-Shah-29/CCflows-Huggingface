import os

from aiflows import logging
from aiflows.backends.api_info import ApiInfo
from aiflows.utils.general_helpers import read_yaml_file, quick_load_api_keys
from aiflows.flow_cache import CACHING_PARAMETERS, clear_cache
from aiflows.utils import serving
from aiflows.utils.colink_utils import start_colink_server
from aiflows.workers import run_dispatch_worker_thread

CACHING_PARAMETERS.do_caching = False  # Set to True to enable caching

logging.set_verbosity_debug()

dependencies = [
    {"url": "aiflows/CodeDebugFlowModule", "revision": os.getcwd()},
]

from aiflows import flow_verse
flow_verse.sync_dependencies(dependencies)

if __name__ == "__main__":
    # Set up a colink server
    cl = start_colink_server()

    # Load flow config
    root_dir = "."
    cfg_path = os.path.join(root_dir, "CodeDebug.yaml")
    cfg = read_yaml_file(cfg_path)

    # Set the API information
    api_information = [ApiInfo(backend_used="openai",
                               api_key=os.getenv("OPENAI_API_KEY"))]

    quick_load_api_keys(cfg, api_information, key="api_infos")

    # Serve the Flow
    serving.recursive_serve_flow(
        cl=cl,
        flow_class_name="flow_modules.aiflows.CodeDebugFlowModule.CodeDebug",
        flow_endpoint="CodeDebug",
    )

    # Start a Worker Thread
    run_dispatch_worker_thread(cl)

    # Mount the flow and get its proxy
    proxy_flow = serving.get_flow_instance(
        cl=cl,
        flow_endpoint="CodeDebug",
        user_id="local",
        config_overrides=cfg
    )

    # Prepare data
    data = {
        "id": 0,
        "problem_description": "Write a function to add two numbers.",
        "input_description": "Provide input as two numbers.",
        "output_description": "The function should return their sum.",
        "io_examples_and_explanation": [
            {"input": [1, 2], "output": 3, "explanation": "1 + 2 equals 3."},
            {"input": [-1, 5], "output": 4, "explanation": "-1 + 5 equals 4."}
        ],
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
    print("~~~~~~Reply from CodeDebugFlow~~~~~~")
    print(reply_data)
