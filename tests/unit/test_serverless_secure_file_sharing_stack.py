import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_secure_file_sharing.serverless_secure_file_sharing_stack import ServerlessSecureFileSharingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_secure_file_sharing/serverless_secure_file_sharing_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessSecureFileSharingStack(app, "serverless-secure-file-sharing")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
