from backend.config.db import Base
from sqlalchemy import String, ForeignKey, Integer, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime

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
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    finish_date: Mapped[date | None] = mapped_column(Date, nullable=True)

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