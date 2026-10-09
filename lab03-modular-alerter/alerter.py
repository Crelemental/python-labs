import logging
import requests
from models import SecurityAlert
from config import config

logger = logging.getLogger(__name__)

def send_alert(alert: SecurityAlert) -> bool:
    payload = alert.model_dump()
    try:
        logger.info(f"Dispatching alert for IP: {alert.source_ip} (Count: {alert.denied_count})")

        response = requests.post(
            str(config.alert_webhook_url),
            json=payload,
            timeout=(4, 10)
        )
        response.raise_for_status()

        logger.info(f"Alert sent successfully to endpoint. Response status code: {response.status_code}")
        return True

    except requests.exceptions.Timeout:
        logger.error(f"Timeout occurred while sending alert for IP: {alert.source_ip}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error response from webhook: {err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Failed to transmit alert to network error: {err}")

    return False