from flow_modules.aiflows.ChatFlowModule import ChatAtomicFlow


class LC_PlanCritic(ChatAtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
