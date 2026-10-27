from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from backend.config.db import Base
from datetime import datetime
from backend.models.book import Book
from backend.models.user import User

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False
    )
    book_id: Mapped[str] = mapped_column(
        String(255), 
        ForeignKey("books.key"), 
        nullable=False
    )
    text_review: Mapped[str | None] = mapped_column(Text, nullable=True )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", lazy="select")
    book:Mapped["Book"] = relationship("Book", lazy="select")