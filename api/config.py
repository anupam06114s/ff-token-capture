import json

def handler(request):
    config = {
        "verAddr": "https://ff-token-captures.vercel.app/api/capture",
        "tokenCapture": True,
        "version": "1.0.0"
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(config)
    }