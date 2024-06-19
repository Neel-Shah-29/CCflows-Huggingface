import logging
from typing import Dict, Any
from aiflows.base_flows import AtomicFlow
from aiflows.interfaces import KeyInterface
from aiflows.messages import FlowMessage
from aiflows.backends.llm_lite import LiteLLMBackend
from aiflows.prompt_template import JinjaPrompt
from aiflows.backends.api_info import ApiInfo
import os
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# class CodeGeneratorFlow(AtomicFlow):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.prompt_template = JinjaPrompt(template=self.flow_config["human_message_prompt_template"]["template"])
#         self.backend = LiteLLMBackend(model_name=self.flow_config["backend"]["model_name"]["openai"])
#         self.input_interface = KeyInterface(keys_to_select=["testing_results_summary"])

#     def run(self, input_message: FlowMessage):
#         input_data = self.input_interface(input_message.data)
#         user_prompt = self.prompt_template.format(**input_data)

#         response = self.backend(messages=[{"role": "user", "content": user_prompt}])
#         generated_code = response[0]["content"]

#         reply_message = self.package_output_message(
#             input_message,
#             response={"code": generated_code}
#         )
#         self.send_message(reply_message)
class CodeGeneratorFlow(AtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Load prompt template from the configuration
        self.prompt_template = JinjaPrompt(template=self.flow_config["human_message_prompt_template"]["template"])
        
        # Prepare API information
        api_key = os.getenv("OPENAI_API_KEY")  # Replace with your method to load API key
        if not api_key:
            raise ValueError("API key for OpenAI is not set. Please set it in the environment variable 'OPENAI_API_KEY'.")
        
        api_infos = [ApiInfo(backend_used="openai", api_key=api_key)]
        
        # Initialize LiteLLMBackend with API information
        self.backend = LiteLLMBackend(api_infos=api_infos, model_name=self.flow_config["backend"]["model_name"]["openai"])
        
        # Define the input interface
        self.input_interface = KeyInterface(keys_to_select=["testing_results_summary"])

    def run(self, input_message: FlowMessage):
        input_data = self.input_interface(input_message.data)
        user_prompt = self.prompt_template.format(**input_data)

        response = self.backend(messages=[{"role": "user", "content": user_prompt}])
        generated_code = response[0]["content"]

        reply_message = self.package_output_message(
            input_message,
            response={"code": generated_code}
        )
        self.send_message(reply_message)
