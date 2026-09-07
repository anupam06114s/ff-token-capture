from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)
tokens = {}

REAL_MAJOR_LOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"

@app.route('/')
def home():
    return "✅ Proxy server is running! Use /MajorLogin"

@app.route('/MajorLogin', methods=['POST', 'GET'])
def major_login():
    if request.method == 'GET':
        return "MajorLogin proxy - send POST with Protobuf data", 200
    
    raw_data = request.get_data()
    print(f"[*] Received {len(raw_data)} bytes from game")
    
    if raw_data:
        tokens['latest'] = {
            'access_token': raw_data.hex()[:64],
            'open_id': 'captured_from_proxy',
            'timestamp': time.time()
        }
        print(f"[+] Raw data stored: {raw_data.hex()[:32]}...")
    
    try:
        headers = {
            "Content-Type": "application/octet-stream",
            "User-Agent": request.headers.get("User-Agent", "FF/1.0")
        }
        response = requests.post(
            REAL_MAJOR_LOGIN_URL,
            data=raw_data,
            headers=headers,
            timeout=10
        )
        print(f"[*] Forwarded to real server, status: {response.status_code}")
        return response.content, response.status_code, {
            "Content-Type": "application/octet-stream"
        }
    except Exception as e:
        print(f"[-] Forward error: {e}")
        return f"Proxy error: {e}", 500

@app.route('/api/config', methods=['GET'])
def config():
    return jsonify({
        "serverLoginUrl": "https://accesstoken-i0dx.onrender.com/MajorLogin",
        "tokenCapture": True,
        "version": "1.0.0"
    })

@app.route('/api/get-token', methods=['GET'])
def get_token():
    data = tokens.get('latest')
    if data:
        return jsonify(data)
    return jsonify({"error": "No token captured yet"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
