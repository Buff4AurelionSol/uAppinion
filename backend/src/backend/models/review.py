from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from backend.config.db import Base
from datetime import datetime
from backend.models.book import Book
from backend.models.user import User
if TYPE_CHECKING:
    from backend.models.user_book import UserBook

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_book_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user_books.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    text_review: Mapped[str | None] = mapped_column(Text, nullable=True )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    user_book: Mapped["UserBook"] = relationship("UserBook", back_populates="review")
