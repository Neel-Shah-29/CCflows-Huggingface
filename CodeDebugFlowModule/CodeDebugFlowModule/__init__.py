# ~~~ Specify the dependencies ~~~
dependencies = [
    {"url": "aiflows/CodeGeneratorFlowModule", "revision": "main"},
    {"url": "aiflows/CodeTestingCriticFlowModule", "revision": "main"},
]
from aiflows import flow_verse

flow_verse.sync_dependencies(dependencies)
# ~~~

from .CodeDebug import CodeDebugFlow