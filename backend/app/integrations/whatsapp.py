"""
Football Intelligence Dashboard - WhatsApp Integration
Uses CallMeBot API for sending WhatsApp messages.
"""

from urllib.parse import quote_plus

import httpx
from loguru import logger

from app.core.config import get_settings

settings = get_settings()


class WhatsAppClient:
    """CallMeBot WhatsApp client."""

    def __init__(self):
        self.base_url = settings.CALLMEBOT_URL

    async def send_message(self, phone: str, apikey: str, message: str) -> bool:
        """Send a WhatsApp message via CallMeBot."""
        try:
            encoded_message = quote_plus(message)
            url = f"{self.base_url}?phone={phone}&apikey={apikey}&text={encoded_message}"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)

            if response.status_code == 200:
                logger.info(f"WhatsApp message sent to {phone}")
                return True
            else:
                logger.error(f"WhatsApp send failed ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            logger.error(f"WhatsApp error for {phone}: {e}")
            return False

    async def send_to_all(self, message: str) -> dict:
        """Send message to all configured recipients."""
        recipients = settings.whatsapp_recipients
        results = {"sent": 0, "failed": 0, "details": []}

        for recipient in recipients:
            success = await self.send_message(
                phone=recipient["phone"],
                apikey=recipient["apikey"],
                message=message,
            )
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
            results["details"].append({
                "phone": recipient["phone"],
                "success": success,
            })

        return results


whatsapp_client = WhatsAppClient()
