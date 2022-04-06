import json
import boto3
from utils import api_response
import os

s3 = boto3.client('s3')
s3_bucket = os.environ["CDN_BUCKET"]

def lambda_handler(event, context):
    print(event)

    # try:
    #     s3.delete_object(
    #         Bucket=s3_bucket,
    #         Key=public_key,
    #     )

    # except Exception as e:
    #     print(e)
    #     return api_response("Error deleting the file", 500)
    
    return api_response()