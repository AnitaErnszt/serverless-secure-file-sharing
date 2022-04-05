import typing
from aws_cdk.aws_lambda import Code, Function, Runtime
from aws_cdk.aws_iam import ServicePrincipal
from aws_cdk import Duration
from aws_cdk.aws_iam import PolicyStatement
from constructs import Construct

default_env = {"PYTHONPATH": "/opt/python:/opt/python/vendor:/var/runtime"}


class LambdaFunction(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        name: str,
        handler: str,
        layers: typing.List = [],
        path: str = "src",
        api_arn: str = None,
        env: dict = {},
        memory_size: int = 128,
        timeout: int = 30,
        permissions: dict = {}
    ):
        super().__init__(scope, id)
        fn_env = {**default_env, **env}

        self.function = Function(
            self,
            id,
            code=Code.from_asset(path),
            environment=fn_env,
            function_name=name,
            handler=handler,
            layers=layers,
            memory_size=memory_size,
            runtime=Runtime.PYTHON_3_9,
            timeout=Duration.seconds(timeout),
        )
        if api_arn:
            self.function.add_permission(
                "API Invoke Permission",
                principal=ServicePrincipal("apigateway.amazonaws.com"),
                action="lambda:InvokeFunction",
                source_arn=api_arn,
            )
        if permissions:
            self.function.add_to_role_policy(PolicyStatement(actions=permissions["actions"], resources=permissions["resources"]))
