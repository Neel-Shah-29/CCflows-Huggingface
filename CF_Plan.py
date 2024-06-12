from flow_modules.aiflows.ChatFlowModule import ChatAtomicFlow


class CF_Plan(ChatAtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
