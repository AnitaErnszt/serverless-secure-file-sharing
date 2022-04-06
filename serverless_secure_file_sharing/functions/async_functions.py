from constructs import Construct
from aws_cdk.aws_lambda_event_sources import SqsEventSource

from serverless_secure_file_sharing.utils import LambdaFunction
from serverless_secure_file_sharing.resources.file_sharing_cdn import FileSharingCDN
from serverless_secure_file_sharing.resources.lambda_layers import LambdaLayers
from serverless_secure_file_sharing.resources.queues import Queues

class AsyncFunctions(object):

    def __init__(
        self,
        scope: Construct,
        file_sharing_cdn: FileSharingCDN,
        lambda_layers: LambdaLayers,
        queues: Queues
    ):

        lambda_env = {
            "CDN_BUCKET": file_sharing_cdn.bucket.bucket_name,
            "DELETE_FILE_QUEUE_URL": queues.delete_file_queue.queue_url
        }

        # ASYNC DELETE FILE #
        async_delete_file_fn = LambdaFunction(
            scope,
            "AsyncDeleteFileLambda",
            "async-delete-file",
            path="src/async/",
            handler="delete_file.lambda_handler",
            env=lambda_env,
            layers=[lambda_layers.base],
        )
        file_sharing_cdn.bucket.grant_delete(async_delete_file_fn.function)
        async_delete_file_fn.function.add_event_source(
            SqsEventSource(queues.delete_file_queue, batch_size=1)
        )