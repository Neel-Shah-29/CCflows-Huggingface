from aiflows.base_flows import SequentialFlow


class CF_CodeDebugCritic(SequentialFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _early_exit(self):
        if self.flow_state.get("all_tests_passed", False):
            self.flow_state["code_feedback"] = None
            return True

        return super()._early_exit()
