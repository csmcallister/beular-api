from aws_cdk import core

from config import Config
from stacks.api import ModelAPIStack
from stacks.notebook import BeularNotebookStack
from stacks.vpc import VpcStack

app = core.App()

# TODO: set account and region using the env property on the stacks

vpc_stack = VpcStack(app, "VpcStack")
sm_stack = BeularNotebookStack(
    app,
    'BeularNotebookStack',
    vpc_stack.vpc,
    **Config.sm_stack
)
# Note that you need to train and deploy a model before creating the API Stack
api_stack = ModelAPIStack(app, "ModelAPIStack", **Config.api_stack)

app.synth()
