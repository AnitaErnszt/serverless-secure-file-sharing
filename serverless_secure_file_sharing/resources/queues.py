from constructs import Construct
from aws_cdk import Duration
from aws_cdk.aws_sqs import Queue

class Queues(object):
    def __init__(self, scope: Construct):
        self.delete_file_queue = Queue(
            scope, 
            "DeleteFileQueue", 
            queue_name="delete-file",
            # Wait 5 minutes before deleting the file
            # delivery_delay=Duration().minutes(5)
        )