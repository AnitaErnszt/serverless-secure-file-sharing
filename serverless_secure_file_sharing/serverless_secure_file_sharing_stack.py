from aws_cdk import (
    Stack,
)
from constructs import Construct
from serverless_secure_file_sharing.resources.api import RestAPI
from serverless_secure_file_sharing.resources.tables import Tables

from serverless_secure_file_sharing.resources.website import Website
from serverless_secure_file_sharing.resources.file_sharing_cdn import FileSharingCDN
from serverless_secure_file_sharing.functions.user_functions import UserFunctions
from serverless_secure_file_sharing.functions.async_functions import AsyncFunctions
from serverless_secure_file_sharing.resources.lambda_layers import LambdaLayers
from serverless_secure_file_sharing.resources.queues import Queues

class ServerlessSecureFileSharingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain = "example.com"
        ssl_cert = "TODO"

        website = Website(self, domain, ssl_cert)
        file_sharing_cdn = FileSharingCDN(self, domain, ssl_cert)
        lambda_layers = LambdaLayers(self)
        tables = Tables(self)
        queues = Queues(self)

        rest_api = RestAPI(self, domain, ssl_cert)

        UserFunctions(
            self,
            file_sharing_cdn=file_sharing_cdn,
            api=rest_api,
            tables=tables,
            lambda_layers=lambda_layers,
            queues=queues
        )

        AsyncFunctions(
            self,
            file_sharing_cdn=file_sharing_cdn,
            lambda_layers=lambda_layers,
            queues=queues
        )