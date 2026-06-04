"""
Football Intelligence Dashboard - Telegram Integration
Uses Telegram Bot API for sending notifications.
"""

import httpx
from loguru import logger

from app.core.config import get_settings

settings = get_settings()


class TelegramClient:
    """Telegram Bot API client."""

    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(
        self, chat_id: str, message: str, parse_mode: str = "Markdown"
    ) -> bool:
        """Send a Telegram message."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": message,
                        "parse_mode": parse_mode,
                    },
                )

            data = response.json()
            if data.get("ok"):
                logger.info(f"Telegram message sent to {chat_id}")
                return True
            else:
                logger.error(f"Telegram send failed: {data}")
                return False
        except Exception as e:
            logger.error(f"Telegram error for {chat_id}: {e}")
            return False

    async def send_to_all(self, message: str) -> dict:
        """Send message to all configured chat IDs."""
        chat_ids = settings.telegram_chat_ids_list
        results = {"sent": 0, "failed": 0, "details": []}

        for chat_id in chat_ids:
            success = await self.send_message(chat_id, message)
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
            results["details"].append({
                "chat_id": chat_id,
                "success": success,
            })

        return results


telegram_client = TelegramClient()
