"""
Football Intelligence Dashboard - Notification Service
Orchestrates sending notifications via WhatsApp, Telegram, and Email.
"""

from datetime import datetime, timezone
from typing import List, Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.telegram import telegram_client
from app.integrations.whatsapp import whatsapp_client
from app.models.notification_log import NotificationLog


class NotificationService:
    """Notification dispatch service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_g3_vs_z3_digest(self, matches: List[dict]) -> dict:
        """Send weekly G3 vs Z3 digest to all channels."""
        message = self._build_g3_z3_message(matches)

        results = {"whatsapp": None, "telegram": None}

        # WhatsApp
        try:
            wa_result = await whatsapp_client.send_to_all(message)
            results["whatsapp"] = wa_result
            await self._log_notification("whatsapp", "all", message, wa_result)
        except Exception as e:
            logger.error(f"WhatsApp notification error: {e}")
            results["whatsapp"] = {"error": str(e)}

        # Telegram
        try:
            tg_result = await telegram_client.send_to_all(message)
            results["telegram"] = tg_result
            await self._log_notification("telegram", "all", message, tg_result)
        except Exception as e:
            logger.error(f"Telegram notification error: {e}")
            results["telegram"] = {"error": str(e)}

        return results

    def _build_g3_z3_message(self, matches: List[dict]) -> str:
        """Build the G3 vs Z3 digest message."""
        lines = [
            "⚽🔥 *G3 vs Z3 — Weekly Highlights* 🔥⚽",
            "",
            "Confrontos entre os 3 primeiros (G3) e os 3 últimos (Z3) da tabela:",
            "",
        ]

        for match in matches:
            emoji = "🟢" if match.get("status") == "NS" else "🏁"
            score = f"{match.get('home_score', '?')} x {match.get('away_score', '?')}" if match.get("status") == "FT" else "vs"

            lines.append(
                f"{emoji} *{match.get('league_name', '')}*"
            )
            lines.append(
                f"   {match.get('home_team', 'Home')} {score} {match.get('away_team', 'Away')}"
            )
            if match.get("match_date"):
                lines.append(f"   📅 {match['match_date']}")
            if match.get("prediction"):
                pred = match["prediction"]
                lines.append(
                    f"   📊 {pred.get('home', 0):.0%} | {pred.get('draw', 0):.0%} | {pred.get('away', 0):.0%}"
                )
            lines.append("")

        if not matches:
            lines.append("📭 Nenhum confronto G3 vs Z3 nesta semana.")
            lines.append("")

        lines.append("_Football Intelligence Dashboard_")
        return "\n".join(lines)

    async def _log_notification(
        self, channel: str, recipient: str, message: str, result: dict
    ) -> None:
        """Log a notification send attempt."""
        status = "sent" if result.get("sent", 0) > 0 else "failed"
        error_msg = result.get("error")

        log = NotificationLog(
            channel=channel,
            recipient=recipient,
            status=status,
            message_content=message[:1000],  # Truncate for storage
            sent_at=datetime.now(timezone.utc),
            error_message=str(error_msg) if error_msg else None,
        )
        self.session.add(log)
        await self.session.flush()
