import json
import boto3
import os
import pydash
from utils import api_response
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
s3_bucket = os.environ["CDN_BUCKET"]
dynamodb = boto3.resource('dynamodb')
inventory_table = dynamodb.Table(os.environ.get("INVENTORY_TABLE"))

def lambda_handler(event, context):
    public_key = pydash.get(event, "pathParameters.id")
    delete_code = pydash.get(event, "queryStringParameters.delete_code")

    try:
        file = inventory_table.get_item(
            Key={"key": public_key}
            ).get("Item", None)
    
    except ClientError as e:
        print(e)
        return api_response(e, 400)

    if not file:
        return api_response("Invalid public key - delete code combination.", 400)

    if file.get("delete_code") == delete_code:
        return api_response("Invalid public key - delete code combination.", 400)

    try:
        file_name = file.get("object_key")
        s3.delete_object(
            Bucket=s3_bucket,
            Key=f"{public_key}/{file_name}",
        )

    except Exception as e:
        print(e)
        return api_response("Error deleting the file", 500)

    try:
        inventory_table.delete_item(
            Key={"key": public_key}
        )
    
    except ClientError as e:
        print(e)
        return api_response(e, 400)
    
    return api_response()