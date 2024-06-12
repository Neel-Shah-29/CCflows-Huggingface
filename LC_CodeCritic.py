from flow_modules.aiflows.ChatFlowModule import ChatAtomicFlow


class LC_CodeCritic(ChatAtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
