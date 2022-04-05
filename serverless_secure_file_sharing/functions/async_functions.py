from aws_cdk import Duration
from constructs import Construct
from aws_cdk.aws_lambda import Code, Function, Runtime
from aws_cdk.aws_s3 import EventType
from aws_cdk.aws_s3_notifications import LambdaDestination

from serverless_secure_file_sharing.resources.file_sharing_cdn import FileSharingCDN

class AsyncFunctions(object):

    def __init__(
        self,
        scope: Construct,
        file_sharing_cdn: FileSharingCDN
    ):
        #####################
        # ASYNC DELETE FILE #
        #####################
        async_delete_file_fn = Function(
            scope,
            "AsyncDeleteFileLambda",
            code=Code.from_asset("src/async/"),
            function_name="async-delete-file",
            handler="delete_file.lambda_handler",
            memory_size=128,
            runtime=Runtime.PYTHON_3_9,
            timeout=Duration.seconds(30),
        )
        file_sharing_cdn.bucket.grant_delete(async_delete_file_fn)
        file_sharing_cdn.bucket.add_event_notification(EventType.OBJECT_CREATED, LambdaDestination(async_delete_file_fn))