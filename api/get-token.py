import json

tokens = {}

def handler(request):
    token_data = tokens.get('latest')
    if token_data:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "access_token": token_data.get('access_token'),
                "open_id": token_data.get('open_id'),
                "timestamp": token_data.get('timestamp')
            })
        }
    return {
        "statusCode": 404,
        "body": json.dumps({"error": "No token captured yet"})
    }