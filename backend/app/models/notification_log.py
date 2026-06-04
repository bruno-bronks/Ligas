"""Notification log model."""

from typing import TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.match import Match


class NotificationLog(Base):
    """Log of all notifications sent."""

    __tablename__ = "notification_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(String(20), nullable=False)  # "whatsapp", "telegram", "email"
    recipient: Mapped[str] = mapped_column(String(200), nullable=False)
    match_id: Mapped[Optional[int]] = mapped_column(ForeignKey("matches.id"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # "sent", "failed", "pending"
    message_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    match: Mapped[Optional["Match"]] = relationship("Match", back_populates="notification_logs")

    def __repr__(self) -> str:
        return f"<NotificationLog {self.channel} -> {self.recipient}: {self.status}>"
