import logging
from config import config
from pathlib import Path
from models import FirewallLog, SecurityAlert
from alerter import send_alert
from parser import parse_log_file


logging.basicConfig(
    level=config.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("main")

def main():
    logger.info("Initializing firewall log processing...")
    log_path = Path(__file__).parent / "firewall.log"

    block_counts = parse_log_file(log_path)

    logger.info("Evaluating brute-force attempts...")
    for ip, count in block_counts.items():
        if count >= config.alert_threshold:
            alert = SecurityAlert(
                source_ip=ip,
                denied_count=count,
                message=f"Detected {count} blocked attempts from IP {ip}. Potential brute-force attack."
            )
            send_alert(alert)
    logger.info("Firewall log processing completed.")
    
if __name__ == "__main__":
    main()