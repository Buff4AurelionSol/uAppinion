from backend.config.db import Base
from sqlalchemy import Table, Column, String, Integer, ForeignKey, UniqueConstraint

book_genre_association = Table(
    "book_genre_association", 
    Base.metadata, 
    Column("book_key", String, ForeignKey("books.key", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("book_key", "genre_id", name="uq_book_genre")

)