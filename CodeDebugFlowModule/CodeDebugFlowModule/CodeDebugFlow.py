import logging
from aiflows.base_flows import CompositeFlow
from aiflows.interfaces import KeyInterface
from aiflows.messages import FlowMessage

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class CodeDebugFlow(CompositeFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_interface_code_generator = KeyInterface(
            keys_to_select=["problem_description", "input_description", "output_description", "io_examples_and_explanation"]
        )
        self.input_interface_code_testing = KeyInterface(
            keys_to_select=["code", "public_tests_individual_io"]
        )
        self.next_state = {
            None: "CodeGenerator",
            "CodeGenerator": "CodeTestingCritic",
            "CodeTestingCritic": "CodeGenerator",
        }

    def set_up_flow_state(self):
        super().set_up_flow_state()
        self.flow_state["last_state"] = None
        self.flow_state["current_round"] = 0
        self.flow_state["all_tests_passed"] = False
        self.flow_state["input_message"] = None


    def register_data_to_state(self, input_message):
        # breakpoint()
        # if  self.flow_state["last_state"] is None:
        #     self.flow_state["last_state"] = "Code_Generator"
        last_state = self.flow_state["last_state"]
        if last_state == None:
            self.flow_state["input_message"] = input_message
        if last_state == "CodeTestingCritic":
            self.flow_state["testing_results_summary"] = input_message.data["testing_results_summary"]
            self.flow_state["all_tests_passed"] = input_message.data["all_tests_passed"]

    def call_code_generator(self, input_message):
        message = self.package_input_message(
            data=self.input_interface_code_generator(self.flow_state),
            dst_flow="CodeGenerator"
        )
        self.subflows["CodeGenerator"].get_reply(message)

    def call_code_testing(self):
        message = self.package_input_message(
            data=self.input_interface_code_testing(self.flow_state),
            dst_flow="CodeTestingCritic"
        )
        self.subflows["CodeTestingCritic"].get_reply(message)


    def generate_reply(self):
        """Generates a reply message with the final state of the flow."""
        if not self.flow_state["input_message"]:
            log.error("No input message found in flow state.")
            return

        response_data = {
            "code": self.flow_state.get("code"),
            "testing_results_summary": self.flow_state.get("testing_results_summary"),
            "all_tests_passed": self.flow_state.get("all_tests_passed"),
            "current_round": self.flow_state.get("current_round")
        }

        log.info("Generating final reply with data: %s", response_data)

        reply_message = self.package_output_message(
            input_message = self.flow_state["input_message"], 
            response=response_data
        )
        self.send_message(reply_message)

    def run(self, input_message):
        self.register_data_to_state(input_message)
        current_state = self.next_state
        if current_state == "CodeGenerator":
            self.call_code_generator()
        elif current_state == "CodeTestingCritic":
            self.call_code_testing()

        if self.flow_state["all_tests_passed"] or self.flow_state["current_round"] >= self.flow_config["max_rounds"]:
            self.generate_reply()
        else:
            self.flow_state["last_state"] = current_state
            self.flow_state["current_round"] += 1
            self.run(input_message)
