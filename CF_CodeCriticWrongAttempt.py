from flow_modules.aiflows.ChatFlowModule import ChatAtomicFlow


class CF_CodeCriticWrongAttempt(ChatAtomicFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
