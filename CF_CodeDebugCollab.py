from aiflows.base_flows import CircularFlow


class CF_CodeDebugCollab(CircularFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _early_exit(self):
        if self.flow_state.get("all_tests_passed", False):
            return True

        return super()._early_exit()
