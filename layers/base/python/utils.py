import json

def api_response(response=None, status_code=200):
    status = "success" if (status_code >= 200 and status_code < 300) else "failure"
    body = {"status": status}
    if status == "failure":
        body["error"] = response
    elif response is not None:
        body["data"] = response
    return {
        "statusCode": status_code,
        "headers": cors_headers(),
        "body": json.dumps(body),
    }


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        "Access-Control-Allow-Headers": "Authorization,Content-Type,Origin",
    }