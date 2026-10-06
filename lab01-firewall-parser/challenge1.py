from pydantic import BaseModel, IPvAnyAddress, ValidationError
from typing import Literal

class LogEntry(BaseModel):
    ip: IPvAnyAddress
    action: Literal["ALLOW", "BLOCK"]
    
logs = [
    "192.168.1.5 ALLOW",
    "10.0.0.4 BLOCK",
    "999.999.999.999 BLOCK",
    "192.168.1.5 BLOCK",
    "172.16.0.2 ALLOW",
    "10.0.0.4 BLOCK",
    "10.0.0.4 GARBAGE_ACTION",
    "10.0.0.4 BLOCK",
]

final_dict = {}

for log in logs:
    raw_ip = log.split(" ")[0]
    raw_action = log.split(" ")[1]

    try:
        log_entry = LogEntry(ip=raw_ip, action=raw_action)
    except ValidationError as e:
        print(f"Invalid log entry: {log}.")
        continue

    if log_entry.action == "BLOCK":
        ip_str = str(log_entry.ip)
        final_dict[ip_str] = final_dict.get(ip_str, 0) + 1
    #if action == "BLOCK":
        #
        # if ip in final_dict:
        #     final_dict[ip] += 1
        # else:
        #     final_dict[ip] = 1
        #
        #final_dict[ip] = final_dict.get(ip, 0) + 1

print(final_dict)

for ip, count in final_dict.items():
	if count > 2:
		print(f"ALERT: BRUTE FORCE by {ip} with {count} blocks!")