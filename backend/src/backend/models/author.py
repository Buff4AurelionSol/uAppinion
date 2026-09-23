from typing import TYPE_CHECKING
from backend.config.db import Base 
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String
from .associations import book_authors
if TYPE_CHECKING:
    from backend.models.book import Book

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship("Book", secondary=book_authors, back_populates="authors")