import aws_cdk as cdk
from constructs import Construct

from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode

class Tables(object):
    def __init__(self, scope: Construct):
        
        self.inventory = Table(scope, "InventoryTable", 
            table_name="inventory-table", 
            partition_key=Attribute(name="key", type=AttributeType.STRING),
            billing_mode=BillingMode.PAY_PER_REQUEST, 
            removal_policy=cdk.RemovalPolicy.DESTROY)