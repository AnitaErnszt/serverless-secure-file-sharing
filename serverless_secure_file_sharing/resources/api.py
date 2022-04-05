import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_apigateway import (
    BasePathMapping,
    DomainName,
    EndpointType,
    StageOptions,
    MethodLoggingLevel,
    BasePathMapping,
    DomainName,
    EndpointType,
    StageOptions,
    MethodLoggingLevel,
    ApiDefinition,
    SpecRestApi,
)
from aws_cdk.aws_s3_assets import Asset

class RestAPI(object):
    def __init__(self, scope: Construct, domain: str, ssl_cert: str):

        # Generate an asset for the API Schema
        asset = Asset(scope, "ApiSchemaAsset", path="schemas/api-schema.yaml")

        # Generate the API
        self.api = SpecRestApi(
            scope,
            "RestAPI",
            api_definition=ApiDefinition.from_inline(
                # Transform the API Schema
                cdk.Fn.transform("AWS::Include", {"Location": asset.s3_object_url})
            ),
            rest_api_name="secure-files-sharing-api",
            deploy_options=StageOptions(logging_level=MethodLoggingLevel.INFO),
            endpoint_types=[EndpointType.EDGE],
        )

        # Get ARN for the api
        self.api_arn = self.api.arn_for_execute_api()

        # # Create the domain name for the API
        # domain_name = f"file-sharing-api.{domain}"

        # domain = DomainName(
        #     scope,
        #     "AdminDomainName",
        #     certificate=ssl_cert,
        #     domain_name=domain_name,
        #     endpoint_type=EndpointType.EDGE,
        # )

        # # Map the base path to the Rest API
        # BasePathMapping(scope, "AdminDomainMapping", domain_name=domain, rest_api=self.api)
