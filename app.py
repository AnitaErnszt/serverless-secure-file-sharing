#!/usr/bin/env python3
import os

import aws_cdk as cdk

from serverless_secure_file_sharing.serverless_secure_file_sharing_stack import ServerlessSecureFileSharingStack

'''
WARNING: Resources are set to be destroyed upon CDK destruction. 
If resources/S3 objects are required to be kept stack should be updated accordingly.
'''

app = cdk.App()

CDK_ENV = cdk.Environment(
    account="831109068910", region="eu-west-1"
)

ServerlessSecureFileSharingStack(app, "ServerlessSecureFileSharingStack", env=CDK_ENV)

app.synth()
