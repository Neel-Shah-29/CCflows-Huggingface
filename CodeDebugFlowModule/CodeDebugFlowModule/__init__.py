# ~~~ Specify the dependencies ~~~
dependencies = [
    {"url": "aiflows/CodeGeneratorFlowModule", "revision": "/home/hadoop_neel/CodeDebugFlowModule/CodeGeneratorFlowModule"},
    {"url": "aiflows/CodeTestingCriticFlowModule", "revision": "/home/hadoop_neel/CodeDebugFlowModule/CodeTestingCritic"},
]
from aiflows import flow_verse

flow_verse.sync_dependencies(dependencies)
# ~~~

from .CodeDebugFlow import CodeDebugFlow