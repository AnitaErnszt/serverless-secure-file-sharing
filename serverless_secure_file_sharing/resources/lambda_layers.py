import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Code, LayerVersion, Runtime

class LambdaLayers(object):
    def __init__(self, scope: Construct):

        self.base = LayerVersion(
            scope,
            "BaseLayer",
            code=Code.from_asset("layers/base"),
            compatible_runtimes=[Runtime.PYTHON_3_9],
            layer_version_name="python-base",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
  