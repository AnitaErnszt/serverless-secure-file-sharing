from aws_cdk import core
from aws_cdk.aws_sqs import Queue

#####
# Class that stores references to queues.
#####
class Queues(object):
    def __init__(self, scope: core.Construct):
        self.delete_file_queue = Queue(
            scope, "DeleteFileQueue", queue_name="delete-file"
        )