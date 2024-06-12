# ~~~ Specify the dependencies ~~~
dependencies = [
    {"url": "aiflows/ChatFlowModule", "revision": "main"},
    {"url": "aiflows/FixedReplyFlowModule", "revision": "main"},
]

from aiflows import flow_verse

flow_verse.sync_dependencies(dependencies)
# ~~~

# ~~~ Codeforces ~~~
# code
from .CF_Code import CF_Code

# code_reflect
from .FixedReply_CodeReflect import FixedReply_CodeReflect
from .CF_CodeReflect import CF_CodeReflect

# code_collab
from .CF_CodeCritic import CF_CodeCritic
from .CF_CodeCollab import CF_CodeCollab

# code_debug
from .CF_CodeTesting import CF_CodeTesting
from .CF_CodeDebug import CF_CodeDebug

# code_debug_collab
from .CF_CodeCriticWrongAttempt import CF_CodeCriticWrongAttempt
from .CF_CodeDebugCritic import CF_CodeDebugCritic
from .CF_CodeDebugCollab import CF_CodeDebugCollab

# plan-code (and plan_oracle-code)
from .CF_Plan import CF_Plan
from .CF_CodeWithPlan import CF_CodeWithPlan
from .CF_Plan_Code import CF_Plan_Code

# plan_reflect-code
from .FixedReply_PlanReflect import FixedReply_PlanReflect
from .CF_PlanReflect import CF_PlanReflect
from .CF_PlanReflect_Code import CF_PlanReflect_Code

# plan_collab-code
from .CF_PlanCritic import CF_PlanCritic
from .CF_PlanCollab import CF_PlanCollab
from .CF_PlanCollab_Code import CF_PlanCollab_Code

# plan_oracle-code_debug_collab
from .CF_CodeCriticWrongAttemptWithPlan import CF_CodeCriticWrongAttemptWithPlan
from .CF_CodeDebugCriticWithPlan import CF_CodeDebugCriticWithPlan
from .CF_CodeDebugCollabWithPlan import CF_CodeDebugCollabWithPlan
# ~~~

# ~~~ LeetCode ~~~
# code
from .LC_Code import LC_Code

# code_reflect
from .LC_CodeReflect import LC_CodeReflect

# code_collab
from .LC_CodeCritic import LC_CodeCritic
from .LC_CodeCollab import LC_CodeCollab

# code_debug
from .LC_CodeTesting import LC_CodeTesting
from .LC_CodeDebug import LC_CodeDebug

# code_debug_collab
from .LC_CodeCriticWrongAttempt import LC_CodeCriticWrongAttempt
from .LC_CodeDebugCritic import LC_CodeDebugCritic
from .LC_CodeDebugCollab import LC_CodeDebugCollab

# plan-code
from .LC_Plan import LC_Plan
from .LC_CodeWithPlan import LC_CodeWithPlan
from .LC_Plan_Code import LC_Plan_Code

# plan_reflect-code
from .LC_PlanReflect import LC_PlanReflect
from .LC_PlanReflect_Code import LC_PlanReflect_Code

# plan_collab-code
from .LC_PlanCritic import LC_PlanCritic
from .LC_PlanCollab import LC_PlanCollab
from .LC_PlanCollab_Code import LC_PlanCollab_Code
# ~~~
