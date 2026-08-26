from http.server import BaseHTTPRequestHandler
import json

tokens = {}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token_data = tokens.get('latest')
        if token_data:
            response_data = {
                "access_token": token_data.get('access_token'),
                "open_id": token_data.get('open_id'),
                "timestamp": token_data.get('timestamp')
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No token captured yet"}).encode('utf-8'))