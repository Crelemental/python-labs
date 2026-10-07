import requests
import json
from pathlib import Path
from pydantic import BaseModel, IPvAnyAddress, ValidationError

log_path = Path(__file__).parent / "firewall.log"

class FirewallLog(BaseModel):
    timestamp: str
    src_ip: IPvAnyAddress
    dst_ip: IPvAnyAddress
    src_port: int
    dst_port: int
    protocol: str
    action: str
    bytes: int

payload = {}

with open(log_path, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        logdict = {}
        for token in line.split():
            if "=" in token:
                key, value = token.split("=", 1)
                logdict[key] = value.strip('"')
                #print("parsed logdict:", logdict)
        try:
            log_entry = FirewallLog(**logdict)
        except ValidationError as e:
             print(f"Invalid log entry: {line}.")
             print(e)
             continue
        if log_entry.action.upper() in ("BLOCK", "DENY"):
            ip_str = str(log_entry.src_ip)
            payload[ip_str] = payload.get(ip_str, 0) + 1

if payload:
    print("Payload to send:")
    print(json.dumps(payload, indent=2))
    r = requests.post("http://httpbin.org/post", json=payload)
    print(f"Response status code: {r.status_code}")
else:
    print("No blocked IPs found in the log.")
