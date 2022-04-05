import json
import boto3

def lambda_handler(event, context):
    '''
    For now this file just logs the event it received.
    '''

    print(event)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "success"
        })
    }