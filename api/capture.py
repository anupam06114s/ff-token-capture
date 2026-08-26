import json
import time
from MajorLoginReq_pb2 import MajorLogin
from MajorLoginRes_pb2 import MajorLoginRes

tokens = {}

def handler(request):
    global tokens
    
    raw = request.get_data()
    print(f"[*] Raw data size: {len(raw)} bytes")
    
    try:
        req = MajorLogin()
        req.ParseFromString(raw)
        
        token = req.access_token
        open_id = req.open_id
        
        if token:
            tokens['latest'] = {
                'access_token': token,
                'open_id': open_id,
                'timestamp': time.time()
            }
            print(f"[+] Token captured: {token[:20]}...")
            print(f"[+] Open ID: {open_id}")
            
    except Exception as e:
        print(f"[-] Decode error: {e}")
    
    # Build response
    res = MajorLoginRes()
    res.account_id = 123456789
    res.token = "session_placeholder"
    res.ttl = 3600
    res.server_url = "https://game.garena.com"
    res.queue_info.Allow = True
    res.queue_info.queue_position = 0
    res.queue_info.need_wait_secs = 0
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/octet-stream"},
        "body": res.SerializeToString()
    }