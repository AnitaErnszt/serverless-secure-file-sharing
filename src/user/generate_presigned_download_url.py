from utils import api_response
import json
import boto3
import os
import pydash
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
s3_bucket = os.environ["CDN_BUCKET"]
dynamodb = boto3.resource("dynamodb")
inventory_table = dynamodb.Table(os.environ.get("INVENTORY_TABLE"))

def lambda_handler(event, context):
    public_key = pydash.get(event, "pathParameters.id")
    access_code = pydash.get(event, "queryStringParameters.access_code")

    try:
        file = inventory_table.get_item(
            Key={"key": public_key}
            ).get("Item", None)
    
    except ClientError as e:
        print(e)
        return api_response(e, 400)

    if not file:
        return api_response("Invalid public key - access code combination.", 400)

    failed_attempts = file.get("attempts", [])
    file_name = file.get("object_key")

    if file.get("access_code") == access_code:
        # If access_code matches file access was successful.
        
        # Create tag in S3
        # Probably not needed as we generate presigned url
        # Original idea was that that we tag the file with the requester's IP address and 
        #     create a policy so the object can only be accessed from that IP address. 
        #     However it doesn't seem to be possible to create a policy based on a parameter?
        s3.put_object_tagging(
            Bucket=s3_bucket,
            Key=f"{public_key}/{file_name}",
            Tagging={
                "TagSet": [
                    {
                        "Key": "accessible",
                        "Value": "current"
                    },
                ]
            }
        )

        try:
            # Create presigned URL. URL will be valid for 5 minutes
            print(f"{public_key}/{file_name}")
            print(s3_bucket)
            presigned_url = s3.generate_presigned_url(
                "get_object", 
                Params={
                    "Bucket": s3_bucket,
                    "Key": f"{public_key}/{file_name}",
                }, 
                ExpiresIn=120000,
                HttpMethod="GET"
            )

            inventory_table.delete_item(
                Key={"key": public_key}
            )

        # Handle error
        except ClientError as e:
            print(e)
            return api_response(e, 400)
        
        return api_response({
                "download_url": presigned_url,
                "file_name": file_name
            })

    # Update dynamodb record with recent file read attempt
    # response = inventory_table.update_item(
    #                 Key={
    #                     'key': public_key
    #                 },
    #                 AttributeUpdates={
    #                     'string': {
    #                         'Value': failed_attempts.append,
    #                         'Action': "PUT"
    #                     }
    #                 }
    #             )
    return api_response("Invalid public key - access code combination.", 400)

    # TODO: check the password
    # -> if not, update item to show unsuccessful attempt

    # Send message to queue to delete file with 5 min delay ???

    # TODO: figure out what happens if it's a large file and the presigned URL expires mid-way download ?

