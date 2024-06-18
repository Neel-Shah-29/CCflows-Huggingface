import logging
from typing import Dict, Any
from aiflows.base_flows import AtomicFlow
from aiflows.interfaces import KeyInterface
from aiflows.messages import FlowMessage
from aiflows.backends.llm_lite import LiteLLMBackend
from aiflows.prompt_template import JinjaPrompt

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class CodeGeneratorFlow(AtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt_template = JinjaPrompt(template=self.flow_config["human_message_prompt_template"]["template"])
        self.backend = LiteLLMBackend(model_name=self.flow_config["backend"]["model_name"]["openai"])
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
