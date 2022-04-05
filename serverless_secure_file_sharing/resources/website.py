import aws_cdk as cdk
from constructs import Construct

from aws_cdk.aws_cloudfront import (
    Behavior,
    CloudFrontWebDistribution,
    CustomOriginConfig,
    OriginProtocolPolicy,
    SourceConfiguration,
    ViewerProtocolPolicy,
)
from aws_cdk.aws_s3 import Bucket, BucketAccessControl

'''
New bucket to be used by the front end
'''
class Website(object):
    def __init__(self, scope: Construct, domain: str, ssl_cert: str) -> None:
        website_domain_name = f"file-sharing.{domain}" # open to suggestions

        self.bucket = Bucket(
            scope,
            "WebsiteBucket",
            access_control=BucketAccessControl.PUBLIC_READ,
            bucket_name=website_domain_name,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            website_index_document="index.html",
            public_read_access=True,
        )

        self.cdn = CloudFrontWebDistribution(
            scope,
            "WebsiteDistribution",
            origin_configs=[
                SourceConfiguration(
                    behaviors=[Behavior(is_default_behavior=True)],
                    custom_origin_source=CustomOriginConfig(
                        domain_name=self.bucket.bucket_website_domain_name,
                        origin_protocol_policy=OriginProtocolPolicy.HTTP_ONLY,
                    ),
                )
            ],
            viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        )