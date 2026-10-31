from typing import TYPE_CHECKING
from backend.config.db import Base
from sqlalchemy import String, ForeignKey, Integer, Date, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date 
if TYPE_CHECKING: 
    from backend.models.review import Review

class UserBook(Base):
    __tablename__ = "user_books"
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True, 
    )
    
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

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    num_pages: Mapped[int | None] = mapped_column(Integer, nullable=True)
    format: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    finish_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    is_reread: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[date | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    ), 

    user: Mapped[str] = relationship("User", lazy="select") 
    book: Mapped[str] = relationship("Book", lazy="select")
    review: Mapped["Review"] = relationship("Review", back_populates="user_book", uselist=False, cascade="all, delete-orphan")