from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, Date, ForeignKey, Boolean
from backend.config.db import Base
from datetime import date

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    book_id: Mapped[str] = mapped_column(String(255), ForeignKey("books.key"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
    num_pages: Mapped[int | None] = mapped_column(Integer, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    finish_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False)
    text_review: Mapped[str | None] = mapped_column(Text, nullable=True )