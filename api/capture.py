from http.server import BaseHTTPRequestHandler
import json
import time
import os
import sys

# Ensure root dir is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from MajorLoginReq_pb2 import MajorLogin
except Exception:
    MajorLogin = None

try:
    from MajorLoginRes_pb2 import MajorLoginRes
except Exception:
    MajorLoginRes = None

tokens = {}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(content_length) if content_length > 0 else b""
        
        token = None
        open_id = None
        
        if MajorLogin and len(raw) > 0:
            try:
                req = MajorLogin()
                req.ParseFromString(raw)
                if req.access_token:
                    token = req.access_token
                if req.open_id:
                    open_id = req.open_id
            except Exception as e:
                print(f"[-] Decode error: {e}")
                
        if token:
            tokens['latest'] = {
                'access_token': token,
                'open_id': open_id or 'N/A',
                'timestamp': time.time()
            }
            print(f"[+] Token captured: {token[:20]}...")
            
        res_body = b""
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
                res_body = res.SerializeToString()
            except Exception as e:
                print(f"[-] Response build error: {e}")
                
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(res_body)