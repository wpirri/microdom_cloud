import asyncio
import httpx
from app.log_utils import get_daily_logger
from app.config_utils import get_config_value
from app.mysql_utils import mysql_execute, mysql_query

logger = get_daily_logger()

async def send_post():
    async with httpx.AsyncClient(timeout=10) as client:
        remote_proto = get_config_value("REMOTE_PROTO", "https")
        remote_host = get_config_value("REMOTE_HOST", "localhost")
        remote_port = get_config_value("REMOTE_PORT", "443")
        target_url = f"{remote_proto}://{remote_host}:{remote_port}/cgi-bin/dompi_cloud_notif.cgi"
        try:
            logger.info(f"POST {target_url}")
            response = await client.post(target_url, json={"service": "microdom_cloud"})
            logger.info(f"Response: {response.status_code}")
            if(response.status_code == 200):
                logger.info(f"POST successful: {response.text}")
        except Exception as e:
            logger.error(f"Error enviando POST: {e}")

async def worker_loop():
    while True:
        await send_post()
        await asyncio.sleep(get_config_value("QUERY_INTERVAL", 5))
        