import logging
from pathlib import Path
from models import FirewallLog

logger = logging.getLogger(__name__)

def parse_log_file(log_path: Path) -> dict[str, int]:
    state_map: dict[str, int] = {}

    if not log_path.exists():
        logger.error(f"Log file not found at {log_path}")
        return state_map

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                tokens = dict(item.split("=") for item in line.split(" "))
                log_entry = FirewallLog(src_ip=tokens.get("src"), action=tokens.get("action"))

                if log_entry.action == "BLOCK":
                    ip_str = str(log_entry.src_ip)
                    state_map[ip_str] = state_map.get(ip_str, 0) + 1

            except Exception as e:
                logger.error(f"Skipping malformed log entry: {line}. Error: {e}")
                continue

    return state_map