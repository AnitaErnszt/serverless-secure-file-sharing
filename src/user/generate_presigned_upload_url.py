import json
import boto3
import uuid
import os
from botocore.exceptions import ClientError
from utils import api_response

s3 = boto3.client('s3')
s3_bucket = os.environ["CDN_BUCKET"]
dynamodb = boto3.resource('dynamodb')
inventory_table = dynamodb.Table(os.environ.get("INVENTORY_TABLE"))

def lambda_handler(event, context):
    payload = json.loads(event["body"])
    
    for key in ["content_type", "file_name"]:
        if not payload.get(key):
            return api_response("Missing required field: '{key}'", 400)

    content_type = payload.get("content_type")
    file_name = payload.get("file_name")
    public_key = uuid.uuid4().hex

    try:
        presigned_url = s3.generate_presigned_url("put_object", {
            "Bucket": s3_bucket,
            "Key": f"{public_key}/{file_name}",
            "ContentType": content_type,
            "CacheControl": "max-age=31104000"
        })

    except ClientError as e:
        print(e)
        return api_response(e, 400)

    
    delete_code = uuid.uuid4().hex
    access_code = payload.get("access_code")

    asset_data = {
        "key": public_key,
        "object_key": file_name,
        "delete_code": delete_code,
        **(
            {
                "access_code": access_code
            } 
            if access_code else {}
        )
    }

    # Add asset to inventory table
    try:
        inventory_table.put_item(Item=asset_data)
    
    except ClientError as e:
        print(e)
        return api_response(e, 400)
    
    return api_response({
        "upload_url": presigned_url,
        "public_key": public_key,
        "delete_code": delete_code,
        "protected": True if access_code else False
    })