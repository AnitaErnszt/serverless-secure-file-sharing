import aws_cdk as cdk
from constructs import Construct

from aws_cdk.aws_s3 import Bucket, BucketEncryption
from aws_cdk.aws_iam import PolicyStatement, Effect, AnyPrincipal

'''
New bucket to be used for the secure files.
'''
class FileSharingCDN(object):
    def __init__(self, scope: Construct, domain: str, ssl_cert: str) -> None:
        secure_bucket = f"secure-files.{domain}" # open to suggestions

        self.bucket = Bucket(
            scope,
            "SecureBucket",
            bucket_name=secure_bucket,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=BucketEncryption.S3_MANAGED
        )

        self.bucket.add_to_resource_policy(PolicyStatement(
            effect=Effect.DENY,
            actions=["s3:GetObject"],
            resources=[self.bucket.arn_for_objects("*")],
            principals=[AnyPrincipal()],
            conditions={
                    "Null": {
                        "s3:ExistingObjectTag/accessible": True
                    }
                }
        ))

        self.bucket.add_to_resource_policy(PolicyStatement(
            effect=Effect.DENY,
            actions=["s3:GetObject"],
            resources=[self.bucket.arn_for_objects("*")],
            conditions={
                "StringNotEquals": {
                    "s3:ExistingObjectTag/accessible": "current"
                },
            },
            principals=[AnyPrincipal()]
        ))

        # TODO: add policy to only allow the lambda to add tagging