from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        config = {
            "verAddr": "https://ff-token-captures.vercel.app/api/capture",
            "tokenCapture": True,
            "version": "1.0.0"
        }
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(config).encode('utf-8'))